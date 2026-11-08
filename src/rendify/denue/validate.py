import hashlib
import json

from pathlib import Path
from typing import Any


class BronzeValidationError(ValueError):
    """Raised when a Bronze extraction fails schema or integrity validation."""


def validate_bronze_response(
        manifest_path: Path,
) -> dict[str, Any]:
    """
    Validate a DENUE Bronze response using its manifest.

    The manifest identifies the response file and expected metadata. The
    function verifies both file integrity and the JSON record shape, then
    returns a compact summary suitable for Airflow task metadata.
    """
    manifest_path = Path(manifest_path)

    if not manifest_path.is_file():
        raise BronzeValidationError("Bronze manifest does not exist")

    try:
        manifest = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise BronzeValidationError("Bronze manifest cannot be read or parsed") from error

    if not isinstance(manifest, dict):
        raise BronzeValidationError("Bronze manifest must be a JSON object")

    # Check the manifest contract before using any metadata to locate or
    # validate the response file.
    required_fields = {
        "source",
        "method",
        "run_id",
        "extracted_at",
        "query_parameters",
        "http",
        "record_count",
        "response_size_bytes",
        "sha256",
        "files",
    }

    missing_fields = required_fields - manifest.keys()

    if missing_fields:
        raise BronzeValidationError("Bronze manifest is missing required fields")

    if manifest["source"] != "DENUE":
        raise BronzeValidationError("Unexpected data source in Bronze manifest")

    if manifest["method"] != "BuscarAreaAct":
        raise BronzeValidationError("Unexpected extraction methoos in Bronze manifest")

    query_parameters = manifest["query_parameters"]

    if not isinstance(query_parameters, dict):
        raise BronzeValidationError("Manifest query_parameters must be an object")

    for key in query_parameters:
        if "token" in key.lower() or "secret" in key.lower():
            raise BronzeValidationError("Credentials must not apear in Bronze metadata")

    http_metadata = manifest["http"]

    if not isinstance(http_metadata, dict):
        raise BronzeValidationError("Manifest http metadata muat be an object")

    if http_metadata.get("status_code") != 200:
        raise BronzeValidationError("DENUE response does not have http status 200")

    files_metadata = manifest["files"]

    if not isinstance(files_metadata, dict):
        raise BronzeValidationError(
            "Manifest files metadata must be an object."
        )

    response_filename = files_metadata.get("response")

    if (
        not isinstance(response_filename, str)
        or not response_filename
        or Path(response_filename).is_absolute()
        or Path(response_filename).name != response_filename
        or response_filename in {".", ".."}
    ):
        raise BronzeValidationError(
            "Invalid response file reference in manifest."
        )

    response_path = manifest_path.parent / response_filename

    if not response_path.is_file():
        raise BronzeValidationError(
            "Bronze response file does not exist."
        )

    try:
        raw_body = response_path.read_bytes()
    except OSError as error:
        raise BronzeValidationError(
            "Bronze response file cannot be read."
        ) from error

    expected_size = manifest["response_size_bytes"]

    if type(expected_size) is not int or expected_size < 0:
        raise BronzeValidationError(
            "Invalid response_size_bytes in manifest."
        )

    if len(raw_body) != expected_size:
        raise BronzeValidationError(
            "Bronze response size does not match its manifest."
        )

    expected_hash = manifest["sha256"]

    if not isinstance(expected_hash, str):
        raise BronzeValidationError(
            "Invalid SHA-256 value in manifest."
        )

    # The checksum detects changes to the raw payload, including formatting
    # changes that would not necessarily alter the parsed records.
    actual_hash = hashlib.sha256(raw_body).hexdigest()

    if actual_hash != expected_hash:
        raise BronzeValidationError(
            "Bronze response checksum does not match its manifest."
        )

    try:
        records = json.loads(raw_body.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise BronzeValidationError(
            "Bronze response is not valid UTF-8 JSON."
        ) from error

    if not isinstance(records, list):
        raise BronzeValidationError(
            "Bronze response must contain a JSON list."
        )

    if not all(isinstance(record, dict) for record in records):
        raise BronzeValidationError(
            "Bronze response contains non-object records."
        )

    expected_count = manifest["record_count"]

    if type(expected_count) is not int or expected_count < 0:
        raise BronzeValidationError(
            "Invalid record_count in manifest."
        )

    if len(records) != expected_count:
        raise BronzeValidationError(
            "Bronze record count does not match its manifest."
        )

    return {
        "manifest_path": str(manifest_path),
        "response_path": str(response_path),
        "record_count": len(records),
        "response_size_bytes": len(raw_body),
        "sha256": actual_hash,
        "status_code": http_metadata["status_code"],
    }
