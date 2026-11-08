
import hashlib
import json
import unittest

from pathlib import Path
from tempfile import TemporaryDirectory

from rendify.denue.validate import (
    BronzeValidationError,
    validate_bronze_response,
)


class TestValidateBronzeResponse(unittest.TestCase):
    """Verify manifest checks and raw-response integrity validation."""

    def setUp(self):
        # Use a complete, deterministic Bronze fixture as the baseline for
        # tests that mutate one validation condition at a time.
        self.temporary_dir = TemporaryDirectory()
        self.addCleanup(self.temporary_dir.cleanup)

        self.root = Path(self.temporary_dir.name)

        self.raw_body = (
            b'[{"Id":"12345","CLEE":"TEST-CLEE"}]'
        )

        self.manifest_path = self.root / "manifest.json"
        self.response_path = self.root / "response.json"

        self.manifest = {
            "source": "DENUE",
            "method": "BuscarAreaAct",
            "run_id": "manual-test-001",
            "extracted_at": "2026-11-03T12:00:00+00:00",
            "query_parameters": {
                "entity": "09",
                "record_start": 1,
                "record_end": 15,
            },
            "http": {
                "status_code": 200,
                "content_type": "application/json",
            },
            "record_count": 1,
            "response_size_bytes": len(self.raw_body),
            "sha256": hashlib.sha256(
                self.raw_body
            ).hexdigest(),
            "files": {
                "response": "response.json",
            },
        }

        self.write_valid_fixture()

    def write_valid_fixture(self):
        self.response_path.write_bytes(self.raw_body)

        self.manifest_path.write_text(
            json.dumps(self.manifest),
            encoding="utf-8",
        )

    def test_validates_bronze_response(self):
        result = validate_bronze_response(
            self.manifest_path
        )

        self.assertEqual(result["record_count"], 1)
        self.assertEqual(result["status_code"], 200)
        self.assertEqual(
            result["sha256"],
            self.manifest["sha256"],
        )

    def test_rejects_missing_response_file(self):
        self.response_path.unlink()

        with self.assertRaises(BronzeValidationError):
            validate_bronze_response(self.manifest_path)

    def test_rejects_checksum_mismatch(self):
        altered_body = (
            b'[{"Id":"12345","CLEE":"TEST-CLEF"}]'
        )

        self.response_path.write_bytes(altered_body)

        with self.assertRaises(BronzeValidationError):
            validate_bronze_response(self.manifest_path)

    def test_rejects_record_count_mismatch(self):
        self.manifest["record_count"] = 2

        self.write_valid_fixture()

        with self.assertRaises(BronzeValidationError):
            validate_bronze_response(self.manifest_path)

    def test_rejects_invalid_json(self):
        invalid_body = b"this is not valid JSON"

        self.response_path.write_bytes(invalid_body)

        self.manifest["response_size_bytes"] = len(invalid_body)
        self.manifest["sha256"] = hashlib.sha256(
            invalid_body
        ).hexdigest()

        self.write_valid_fixture()

        with self.assertRaises(BronzeValidationError):
            validate_bronze_response(self.manifest_path)


if __name__ == "__main__":
    unittest.main()
