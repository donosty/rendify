"""Validation gates for a Bronze DENUE sample."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class DataQualityError(RuntimeError):
    """Raised when the Bronze sample fails a blocking quality rule."""


def validate_bronze_manifest(
    manifest_path: str | Path,
    required_fields: tuple[str, ...] = ("Id", "CLEE"),
) -> dict[str, Any]:
    """Check manifest, file integrity, JSON structure and critical identifiers."""
    path = Path(manifest_path)
    if not path.is_file():
        raise DataQualityError("Bronze manifest does not exist.")

    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        raise DataQualityError("Bronze manifest is not readable valid JSON.") from None

    if manifest.get("result_status") != "success":
        raise DataQualityError(
            f"Bronze run status is not successful: {manifest.get('result_status', 'missing')}."
        )

    response_name = manifest.get("response_file")
    if not response_name or Path(response_name).name != response_name:
        raise DataQualityError("Manifest response_file is missing or unsafe.")
    response_path = path.parent / response_name
    if not response_path.is_file():
        raise DataQualityError("Bronze response file referenced by the manifest is missing.")

    raw_body = response_path.read_bytes()
    actual_sha256 = hashlib.sha256(raw_body).hexdigest()
    if actual_sha256 != manifest.get("response_sha256"):
        raise DataQualityError("Bronze response checksum does not match the manifest.")

    try:
        payload = json.loads(raw_body.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise DataQualityError("Bronze response is not valid UTF-8 JSON.") from None

    if not isinstance(payload, list) or any(not isinstance(row, dict) for row in payload):
        raise DataQualityError("Bronze response must be a JSON list of objects.")
    if len(payload) != manifest.get("record_count"):
        raise DataQualityError("Manifest record_count does not match the Bronze response.")
    if len(payload) == 0:
        raise DataQualityError("The sample response is empty; inspect query and API result.")

    observed_fields = {key for row in payload for key in row}
    missing_fields = sorted(set(required_fields) - observed_fields)
    if missing_fields:
        raise DataQualityError(
            "Required identifier fields are absent from the sample: "
            + ", ".join(missing_fields)
        )

    rows_missing_ids = sum(
        1 for row in payload
        if not str(row.get("Id", "")).strip() or not str(row.get("CLEE", "")).strip()
    )
    unique_ids = {
        str(row.get("Id", "")).strip()
        for row in payload if str(row.get("Id", "")).strip()
    }
    duplicate_id_count = len(payload) - len(unique_ids)
    if rows_missing_ids:
        raise DataQualityError(f"{rows_missing_ids} records have missing Id or CLEE values.")

    return {
        "run_id": manifest["run_id"],
        "manifest_path": str(path.resolve()),
        "record_count": len(payload),
        "observed_fields": sorted(observed_fields),
        "duplicate_id_count": duplicate_id_count,
        "checksum_valid": True,
        "quality_status": "passed_with_warnings" if duplicate_id_count else "passed",
    }
