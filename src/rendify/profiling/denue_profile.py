"""Create a compact quality profile for a saved DENUE sample."""
from __future__ import annotations

import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROFILE_FIELDS = (
    "Id", "CLEE", "Nombre", "Clase_actividad", "Estrato", "Tipo", "Colonia",
    "CP", "Ubicacion", "AreaGeo", "AGEB", "Manzana", "Longitud", "Latitud",
    "Fecha_Alta",
)


def create_profile(
    manifest_path: str | Path,
    reports_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Profile field presence, nulls, types and selected source-specific checks."""
    manifest_file = Path(manifest_path)
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    if manifest.get("result_status") != "success":
        raise ValueError("Cannot profile a failed DENUE extraction.")

    response_name = manifest.get("response_file")
    if not response_name or Path(response_name).name != response_name:
        raise ValueError("Manifest response_file is missing or unsafe.")
    payload = json.loads(
        (manifest_file.parent / response_name).read_text(encoding="utf-8-sig")
    )
    if not isinstance(payload, list) or any(not isinstance(row, dict) for row in payload):
        raise ValueError("Expected a JSON list of records.")

    fields = sorted({key for row in payload for key in row})
    null_counts = {}
    observed_types = {}
    for field in fields:
        values = [row.get(field) for row in payload]
        null_counts[field] = sum(
            value is None or (isinstance(value, str) and not value.strip())
            for value in values
        )
        observed_types[field] = sorted(
            {type(value).__name__ for value in values if value is not None}
        )

    profile: dict[str, Any] = {
        "profile_version": "1.0",
        "source_id": manifest.get("source_id"),
        "dataset_id": manifest.get("dataset_id"),
        "run_id": manifest.get("run_id"),
        "profiled_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "record_count": len(payload),
        "fields_present": fields,
        "candidate_fields_not_observed": sorted(set(PROFILE_FIELDS) - set(fields)),
        "null_counts": null_counts,
        "observed_types": observed_types,
        "duplicate_id_count": None,
        "records_missing_id_or_clee": None,
        "coordinates_missing": None,
        "coordinates_invalid": None,
        "interpretation": [
            "This profile describes only this API response sample.",
            "An unobserved candidate field requires review; it does not prove that the API never provides it.",
            "DENUE establishment counts and staff-size strata are not measures of profit or business success.",
        ],
    }

    ids = [str(row.get("Id", "")).strip() for row in payload if str(row.get("Id", "")).strip()]
    profile["duplicate_id_count"] = len(ids) - len(set(ids))
    profile["records_missing_id_or_clee"] = sum(
        1 for row in payload
        if not str(row.get("Id", "")).strip() or not str(row.get("CLEE", "")).strip()
    )

    coords_missing = 0
    coords_invalid = 0
    for row in payload:
        lat, lon = row.get("Latitud"), row.get("Longitud")
        if lat in (None, "") or lon in (None, ""):
            coords_missing += 1
            continue
        try:
            lat_float, lon_float = float(lat), float(lon)
        except (TypeError, ValueError):
            coords_invalid += 1
            continue
        if not (-90 <= lat_float <= 90 and -180 <= lon_float <= 180):
            coords_invalid += 1
    profile["coordinates_missing"] = coords_missing
    profile["coordinates_invalid"] = coords_invalid

    for field in ("Clase_actividad", "Estrato", "Tipo", "Colonia", "CP", "Ubicacion"):
        counts = Counter(
            str(row.get(field)).strip()
            for row in payload if row.get(field) not in (None, "")
        )
        profile.setdefault("top_values", {})[field] = [
            {"value": value, "count": count}
            for value, count in counts.most_common(10)
        ]

    output_dir = Path(reports_dir or os.getenv("RENDIFY_REPORTS_DIR", "reports/generated"))
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / f"denue_profile_{manifest.get('run_id', 'unknown')}.json"
    report_path.write_text(
        json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    profile["report_path"] = str(report_path.resolve())
    return profile
