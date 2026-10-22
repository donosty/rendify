import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from rendify.denue.client import DenueAreaActivityQuery
from rendify.denue.extract import extract_sample


class TestDenueExtract(unittest.TestCase):
    @patch("rendify.denue.extract.fetch_page")
    def test_extract_writes_original_body_and_manifest_without_token(self, mocked_fetch):
        rows = [
            {
                "Id": "1001",
                "CLEE": "CLEE-1001",
                "Clase_actividad": "Cafeterías",
                "Latitud": "19.4",
                "Longitud": "-99.1",
            }
        ]
        raw = json.dumps(rows, ensure_ascii=False).encode("utf-8")
        mocked_fetch.return_value = (raw, rows, 200, "application/json")

        with tempfile.TemporaryDirectory() as temp_dir:
            result = extract_sample(
                output_root=temp_dir,
                token="super-secret-test-token",
                query=DenueAreaActivityQuery(),
            )
            manifest_path = Path(result["manifest_path"])
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            original = (manifest_path.parent / manifest["response_file"]).read_bytes()

            self.assertEqual(original, raw)
            self.assertEqual(manifest["record_count"], 1)
            self.assertEqual(manifest["result_status"], "success")
            self.assertNotIn("super-secret-test-token", json.dumps(manifest))
            self.assertNotIn("token", json.dumps(manifest).lower())
            self.assertEqual(result["record_count"], 1)

    def test_missing_token_fails_without_making_a_request(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ValueError):
                extract_sample(output_root=tempfile.gettempdir(), token=None)


if __name__ == "__main__":
    unittest.main()
