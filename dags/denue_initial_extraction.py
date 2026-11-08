
import os

from datetime import datetime, timedelta, timezone
from pathlib import Path

from airflow.sdk import dag, get_current_context, task

from rendify.denue.extract import extract_denue_to_bronze
from rendify.denue.validate import validate_bronze_response


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

    @task(task_id="validate_bronze")
    def validate_bronze(manifest_path: str) -> dict:
        """Validate the Bronze extraction referenced by its manifest."""

        result = validate_bronze_response(
            Path(manifest_path)
        )

        return result

    manifest_path = extract_denue()

    validate_bronze(manifest_path)


denue_initial_extraction()
