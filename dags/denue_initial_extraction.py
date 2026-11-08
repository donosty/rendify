
import os

from datetime import datetime, timedelta, timezone
from pathlib import Path

from airflow.sdk import dag, get_current_context, task

from rendify.denue.extract import extract_denue_to_bronze
from rendify.denue.validate import validate_bronze_response


# Shared filesystem location where the extractor writes the raw response and
# its manifest. The validation task reads the manifest from this same volume.
BRONZE_ROOT = Path("/opt/airflow/data/bronze/denue")


@dag(
    dag_id="denue_initial_extraction",
    description="Initial DENUE extraction and Bronze validation for Rendify.",
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["rendify", "denue", "bronze"],
)
def denue_initial_extraction():

    # This task returns only the manifest path; the response itself remains in
    # Bronze instead of being serialized into Airflow's XCom backend.
    @task(
        task_id="extract_denue",
        retries=2,
        retry_delay=timedelta(minutes=2),
    )
    def extract_denue() -> str:
        """Extract DENUE data and persist the original response in Bronze."""

        token = os.environ.get("DENUE_API_TOKEN")

        if not token or not token.strip():
            raise RuntimeError(
                "DENUE_API_TOKEN is not configured in the Airflow worker."
            )

        context = get_current_context()
        run_id = context["dag_run"].run_id

        # "0" means no filter for the DENUE dimensions. This initial run
        # intentionally requests a small sample (records 1 through 15) to
        # verify connectivity and the Bronze persistence contract.
        manifest_path = extract_denue_to_bronze(
            token=token,
            bronze_root=BRONZE_ROOT,
            run_id=run_id,
            entity="09",
            municipality="0",
            locality="0",
            ageb="0",
            block="0",
            sector="0",
            subsector="0",
            branch="0",
            class_code="0",
            establishment_name="0",
            record_start=1,
            record_end=15,
            establishment_id="0",
        )

        return str(manifest_path)

    # Validation checks the manifest, response metadata, size, checksum, and
    # record count before downstream processing can consume this extraction.
    @task(task_id="validate_bronze")
    def validate_bronze(manifest_path: str) -> dict:
        """Validate the Bronze extraction referenced by its manifest."""

        result = validate_bronze_response(
            Path(manifest_path)
        )

        return result

    # Passing the returned path creates the dependency: validation runs only
    # after extraction has completed successfully.
    manifest_path = extract_denue()

    validate_bronze(manifest_path)


denue_initial_extraction()
