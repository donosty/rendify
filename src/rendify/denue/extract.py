"""Bronze extraction for a small DENUE proof of concept."""
from __future__ import annotations

import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from rendify.denue.client import DenueApiError, DenueAreaActivityQuery, fetch_page


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def extract_sample(
    output_root: str | Path | None = None,
    token: str | None = None,
    query: DenueAreaActivityQuery | None = None,
    timeout: float = 30.0,
) -> dict[str, Any]:
    """Extract one DENUE page into Bronze and create a safe manifest.

    The successful source body is preserved in a JSON file. The manifest and
    returned object do not contain the API token or a token-bearing URL.
    """
    api_token = token or os.getenv("DENUE_API_TOKEN")
    if not api_token:
        raise ValueError("DENUE_API_TOKEN is not set in the process environment.")

    denue_query = query or DenueAreaActivityQuery()
    denue_query.validate()

    data_root = Path(output_root or os.getenv("RENDIFY_DATA_DIR", "data")).expanduser()
    started_at = _utc_now()
    extraction_date = started_at.strftime("%Y-%m-%d")
    run_id = f"{started_at.strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}"
    run_dir = (
        data_root / "bronze" / "denue"
        / f"extraction_date={extraction_date}" / f"run_id={run_id}"
    )
    run_dir.mkdir(parents=True, exist_ok=False)
    manifest_path = run_dir / "manifest.json"

    manifest: dict[str, Any] = {
        "manifest_version": "1.0",
        "source_id": "SRC-DENUE",
        "dataset_id": "denue_establishments",
        "source_provider": "INEGI",
        "source_method": "BuscarAreaAct",
        "source_api_base": "https://www.inegi.org.mx/app/api/denue/v1/consulta/BuscarAreaAct/",
        "query_parameters": denue_query.to_manifest_dict(),
        "run_id": run_id,
        "extraction_started_at": _iso_utc(started_at),
        "extraction_finished_at": None,
        "code_version": os.getenv("RENDIFY_CODE_VERSION", "unknown"),
        "contract_version": "unconfirmed-denue-sample-v0",
        "result_status": "running",
        "http_status": None,
        "content_type": None,
        "record_count": None,
        "response_file": None,
        "response_bytes": None,
        "response_sha256": None,
        "observed_fields": [],
        "notes": [
            "Single-page proof of concept only; not a full extraction.",
            "Schema is provisional until confirmed against a real response.",
        ],
    }

    try:
        raw_body, rows, http_status, content_type = fetch_page(
            query=denue_query, token=api_token, timeout=timeout
        )
        response_name = f"response_{denue_query.start_record:06d}_{denue_query.end_record:06d}.json"
        response_path = run_dir / response_name
        response_path.write_bytes(raw_body)
        observed_fields = sorted({key for row in rows for key in row.keys()})
        manifest.update({
            "extraction_finished_at": _iso_utc(_utc_now()),
            "result_status": "success",
            "http_status": http_status,
            "content_type": content_type,
            "record_count": len(rows),
            "response_file": response_name,
            "response_bytes": len(raw_body),
            "response_sha256": hashlib.sha256(raw_body).hexdigest(),
            "observed_fields": observed_fields,
        })
        _write_json(manifest_path, manifest)
    except Exception as exc:
        manifest.update({
            "extraction_finished_at": _iso_utc(_utc_now()),
            "result_status": "failed",
            "error_type": type(exc).__name__,
            "error_message": str(exc)[:300],
        })
        _write_json(manifest_path, manifest)
        raise

    return {
        "run_id": run_id,
        "manifest_path": str(manifest_path.resolve()),
        "record_count": len(rows),
        "result_status": "success",
    }
