"""Run the small DENUE Bronze proof of concept outside Airflow."""
from __future__ import annotations

import argparse
import json
import logging

from rendify.denue.client import DenueAreaActivityQuery
from rendify.denue.extract import extract_sample
from rendify.denue.validate import validate_bronze_manifest
from rendify.profiling.denue_profile import create_profile


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entity-code", default="09", help="Two-digit INEGI entity code (default: CDMX 09).")
    parser.add_argument("--start-record", type=int, default=1, help="First record to request (default: 1).")
    parser.add_argument("--end-record", type=int, default=15, help="Last record to request (default: 15).")
    parser.add_argument("--output-root", default=None, help="Data root; defaults to RENDIFY_DATA_DIR or data/.")
    parser.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout in seconds.")
    return parser


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = build_parser().parse_args()
    query = DenueAreaActivityQuery(
        entity_code=args.entity_code,
        start_record=args.start_record,
        end_record=args.end_record,
    )
    result = extract_sample(
        output_root=args.output_root,
        query=query,
        timeout=args.timeout,
    )
    validation = validate_bronze_manifest(result["manifest_path"])
    profile = create_profile(result["manifest_path"])
    summary = {
        "run_id": result["run_id"],
        "record_count": result["record_count"],
        "manifest_path": result["manifest_path"],
        "quality_status": validation["quality_status"],
        "duplicate_id_count": validation["duplicate_id_count"],
        "profile_path": profile["report_path"],
        "observed_fields": profile["fields_present"],
        "candidate_fields_not_observed": profile["candidate_fields_not_observed"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
