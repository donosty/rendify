import hashlib
import json
import unittest

from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from rendify.denue.client import DenueAPIResponse
from rendify.denue.extract import save_bronze_response, extract_denue_to_bronze


class TestSaveBronzeResponse(unittest.TestCase):
    """Verify Bronze persistence and the extraction-to-storage boundary."""

    def setUp(self):
        # Keep the fixture byte-for-byte stable so checksum and preservation
        # assertions test the storage contract rather than JSON formatting.
        self.raw_body = b'[{"Id":"12345","CLEE":"TEST-CLEE"}]'

        self.records = [
            {
                "Id": "12345",
                "CLEE": "TEST-CLEE",
            }
        ]

        self.response = DenueAPIResponse(
            status_code=200,
            content_type="application/json",
            raw_body=self.raw_body,
            records=self.records
        )

        self.extracted_at = datetime(
            2026,
            11,
            3,
            12,
            0,
            0,
            tzinfo=timezone.utc
        )

    def test_saves_original_response_and_manifest(self):

        with TemporaryDirectory() as temporary_dir:
            bronze_root = Path(temporary_dir)

            manifest_path = save_bronze_response(
                self.response,
                bronze_root=bronze_root,
                run_id="manual-test-001",
                query_parameters={
                    "entity": "09",
                    "record_start": 1,
                    "record_end": 15
                },
                extracted_at=self.extracted_at
            )

            response_path = manifest_path.parent / "response.json"

            self.assertTrue(response_path.exists())
            self.assertTrue(manifest_path.exists())

            #The raw response must remain exactly the same
            self.assertEqual(
                response_path.read_bytes(),
                self.raw_body
            )

            manifest = json.loads(
                manifest_path.read_text(encoding="utf-8")
            )

            self.assertEqual(manifest["source"], "DENUE")
            self.assertEqual(manifest["method"], "BuscarAreaAct")
            self.assertEqual(manifest["record_count"], 1)
            self.assertEqual(manifest["http"]["status_code"], 200)

            expected_hash = hashlib.sha256(
                self.raw_body
            ).hexdigest()

            self.assertEqual(
                manifest["sha256"],
                expected_hash
            )

            self.assertEqual(
                manifest["run_id"],
                "manual-test-001"
            )

    def test_rejects_credentials_in_query_parameters(self):

        with TemporaryDirectory() as temporary_dir:
            with self.assertRaises(ValueError):
                save_bronze_response(
                    self.response,
                    bronze_root=Path(temporary_dir),
                    run_id="manual-test-002",
                    query_parameters={
                        "entity": "09",
                        "DENUE_API_TOKEN": "SECRET"
                    },
                    extracted_at=self.extracted_at
                )

    def test_rejects_naive_datetime(self):

        with TemporaryDirectory() as temporary_dir:

            with self.assertRaises(ValueError):

                save_bronze_response(
                    self.response,
                    bronze_root=Path(temporary_dir),
                    run_id="manual-test-003",
                    query_parameters={"entity": "09"},
                    extracted_at=datetime(2026, 11, 3),
                    )

    @patch("rendify.denue.extract.fetch_buscar_area_act")
    def test_extracts_and_persists_response(self, mock_fetch):
        mock_fetch.return_value = self.response

        with TemporaryDirectory() as temporary_dir:
            manifest_path = extract_denue_to_bronze(
                token="TEST_TOKEN",
                bronze_root=Path(temporary_dir),
                run_id="manual-test-004",
                extracted_at=self.extracted_at
            )

            mock_fetch.assert_called_once()
            call_parameters = mock_fetch.call_args.kwargs

            self.assertEqual(call_parameters["entity"], "09")
            self.assertEqual(call_parameters["record_start"], 1)
            self.assertEqual(call_parameters["record_end"], 15)
            self.assertEqual(call_parameters["token"], "TEST_TOKEN")

            response_path = manifest_path.parent / "response.json"

            self.assertEqual(
                response_path.read_bytes(),
                self.raw_body,
            )

            manifest = json.loads(
                manifest_path.read_text(encoding="utf-8")
            )

            self.assertNotIn(
                "token",
                manifest["query_parameters"],
            )


            
if __name__ == "__main__":
    unittest.main()