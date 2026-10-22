"""First Rendify DENUE proof-of-concept DAG.

Keep network calls and data processing inside task functions, not at DAG parse
time. All tasks must share configured data and reports volumes.
"""
from datetime import timedelta

import pendulum
from airflow.sdk import dag, task


@dag(
    dag_id="rendify_denue_initial_extraction",
    schedule=None,
    start_date=pendulum.datetime(2026, 10, 21, tz="UTC"),
    catchup=False,
    max_active_runs=1,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=2)},
    tags=["rendify", "denue", "bronze", "data-quality"],
)
def rendify_denue_initial_extraction():
    @task
    def extract_bronze() -> dict:
        from rendify.denue.extract import extract_sample
        return extract_sample()

    @task
    def validate_bronze(extraction_result: dict) -> dict:
        from rendify.denue.validate import validate_bronze_manifest
        result = validate_bronze_manifest(extraction_result["manifest_path"])
        return {
            **extraction_result,
            "quality_status": result["quality_status"],
            "duplicate_id_count": result["duplicate_id_count"],
        }

    @task
    def profile_bronze(validation_result: dict) -> dict:
        from rendify.profiling.denue_profile import create_profile
        result = create_profile(validation_result["manifest_path"])
        return {
            "run_id": result["run_id"],
            "record_count": result["record_count"],
            "report_path": result["report_path"],
            "quality_status": validation_result["quality_status"],
        }

    extracted = extract_bronze()
    validated = validate_bronze(extracted)
    profile_bronze(validated)


rendify_denue_initial_extraction()
