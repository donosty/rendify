import hashlib
import json
import re

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from rendify.denue.client import (
    DenueAPIResponse, 
    fetch_buscar_area_act
)

def _normalize_run_id(run_id: str) -> str:
    """Convert an Airflow run ID into a safe, non-traversing directory name."""

    if not run_id or not run_id.strip():
        raise ValueError("run_id cannot be empty")

    safe_run_id = re.sub(r"[^a-zA-Z0-9._-]", "_", run_id)

    if safe_run_id in {".", ".."}:
        raise ValueError("Invalid run_id.")

    return safe_run_id


def save_bronze_response(
    response: DenueAPIResponse,
    *,
    bronze_root: Path,
    run_id: str,
    query_parameters: dict[str, Any],
    extracted_at: datetime | None = None
) -> Path:
    """
    Persist the original response and metadata manifest as one Bronze unit.

    The response is written before the manifest so a manifest only appears
    after the payload is available and can be validated.
    """

    if extracted_at is None:
        extracted_at = datetime.now(timezone.utc)

    if(
        extracted_at.tzinfo is None or
        extracted_at.utcoffset() is None
    ):
        raise ValueError("extracted_at must be timezone.aware")

    extracted_at = extracted_at.astimezone(timezone.utc)

    if not isinstance(query_parameters, dict):
        raise ValueError("query_parameters must be a dictionary")

    # Prevent credentials from being included in query metadata.
    for key in query_parameters:
        if "token" in key.lower() or "secret" in key.lower():
            raise ValueError(
                "Credentials cannot be included in query_parameters"
            )

    safe_run_id = _normalize_run_id(run_id)

    extraction_date = extracted_at.date().isoformat()

    extraction_dir = (
        bronze_root /
        f"extraction_date={extraction_date}" /
        f"run_id={safe_run_id}"
    )

    extraction_dir.mkdir(parents=True, exist_ok=True)

    response_path = extraction_dir / "response.json"
    manifest_path = extraction_dir / "manifest.json"

    raw_body = response.raw_body

    response_sha256 = hashlib.sha256(raw_body).hexdigest()

    manifest = {
        "source": "DENUE",
        "method": "BuscarAreaAct",
        "run_id": run_id,
        "extracted_at": extracted_at.isoformat(),
        "extraction_date": extraction_date,
        "query_parameters": query_parameters,
        "http": {
            "status_code": response.status_code,
            "content_type": response.content_type
        },
        "record_count": len(response.records),
        "response_size_bytes": len(raw_body),
        "sha256": response_sha256,
        "files": {
            "response": "response.json",
        }
    }

    manifest_bytes = json.dumps(
        manifest,
        ensure_ascii=False,
        indent=2
    ).encode("utf-8")

    # Write the response first, preserving its original bytes.
    response_tmp = extraction_dir / "response.json.tmp"
    response_tmp.write_bytes(raw_body)
    response_tmp.replace(response_path)

    # Write the manifest last so it describes a completed response file.
    manifest_tmp = extraction_dir / "manifest.json.tmp"
    manifest_tmp.write_bytes(manifest_bytes)
    manifest_tmp.replace(manifest_path)

    return manifest_path


def extract_denue_to_bronze(
    *,
    token: str,
    bronze_root: Path,
    run_id: str,
    entity: str = "09",
    municipality: str = "0",
    locality: str = "0",
    ageb: str = "0",
    block: str = "0",
    sector: str = "0",
    subsector: str = "0",
    branch: str = "0",
    class_code: str = "0",
    establishment_name: str = "0",
    record_start: int = 1,
    record_end: int = 15,
    establishment_id: str = "0",
    timeout: float = 30.0,
    extracted_at: datetime | None = None,
) -> Path:
    """
    Fetch a DENUE sample, build auditable query metadata, and persist it.

    Only the manifest path is returned; the potentially larger response stays
    in the Bronze filesystem rather than being passed through task metadata.
    """

    response = fetch_buscar_area_act(
        entity=entity,
        municipality=municipality,
        locality=locality,
        ageb=ageb,
        block=block,
        sector=sector,
        subsector=subsector,
        branch=branch,
        class_code=class_code,
        establishment_name=establishment_name,
        record_start=record_start,
        record_end=record_end,
        establishment_id=establishment_id,
        token=token,
        timeout=timeout,
    )

    query_parameters = {
        "entity": entity,
        "municipality": municipality,
        "locality": locality,
        "ageb": ageb,
        "block": block,
        "sector": sector,
        "subsector": subsector,
        "branch": branch,
        "class_code": class_code,
        "establishment_name": establishment_name,
        "record_start": record_start,
        "record_end": record_end,
        "establishment_id": establishment_id,
    }

    return save_bronze_response(
        response,
        bronze_root=bronze_root,
        run_id=run_id,
        query_parameters=query_parameters,
        extracted_at=extracted_at,
    )
