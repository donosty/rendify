import json
import tempfile
import unittest
from pathlib import Path

from rendify.profiling.denue_profile import create_profile


class TestDenueProfile(unittest.TestCase):
    def test_profile_records_fields_nulls_and_invalid_coordinates(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "bronze"
            root.mkdir()
            rows = [
                {"Id": "1", "CLEE": "A", "Latitud": "19.4", "Longitud": "-99.1", "Estrato": "0 a 5 personas"},
                {"Id": "2", "CLEE": "B", "Latitud": "bad", "Longitud": "", "Estrato": ""},
            ]
            (root / "response.json").write_text(json.dumps(rows), encoding="utf-8")
            manifest = {
                "result_status": "success",
                "source_id": "SRC-DENUE",
                "dataset_id": "denue_establishments",
                "run_id": "profile-test",
                "record_count": len(rows),
                "response_file": "response.json",
            }
            manifest_path = root / "manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = create_profile(
                manifest_path, reports_dir=Path(temp_dir) / "reports"
            )
            self.assertEqual(result["record_count"], 2)
            self.assertEqual(result["records_missing_id_or_clee"], 0)
            self.assertEqual(result["coordinates_missing"], 1)
            self.assertEqual(result["coordinates_invalid"], 0)
            self.assertTrue(Path(result["report_path"]).is_file())


if __name__ == "__main__":
    unittest.main()
