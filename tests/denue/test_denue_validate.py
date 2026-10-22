import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from rendify.denue.validate import DataQualityError, validate_bronze_manifest


class TestValidateBronzeManifest(unittest.TestCase):
    def _write_run(self, root: Path, rows: list[dict]) -> Path:
        response = json.dumps(rows).encode("utf-8")
        response_name = "response_000001_000015.json"
        (root / response_name).write_bytes(response)
        manifest = {
            "run_id": "test-run",
            "result_status": "success",
            "record_count": len(rows),
            "response_file": response_name,
            "response_sha256": hashlib.sha256(response).hexdigest(),
        }
        manifest_path = root / "manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        return manifest_path

    def test_valid_sample_passes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_path = self._write_run(
                Path(temp_dir), [{"Id": "1", "CLEE": "A"}, {"Id": "2", "CLEE": "B"}]
            )
            result = validate_bronze_manifest(manifest_path)
            self.assertEqual(result["record_count"], 2)
            self.assertEqual(result["quality_status"], "passed")
            self.assertTrue(result["checksum_valid"])

    def test_checksum_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_path = self._write_run(Path(temp_dir), [{"Id": "1", "CLEE": "A"}])
            (Path(temp_dir) / "response_000001_000015.json").write_text("[]", encoding="utf-8")
            with self.assertRaises(DataQualityError):
                validate_bronze_manifest(manifest_path)

    def test_missing_id_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_path = self._write_run(Path(temp_dir), [{"Id": "1"}])
            with self.assertRaises(DataQualityError):
                validate_bronze_manifest(manifest_path)

    def test_empty_response_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_path = self._write_run(Path(temp_dir), [])
            with self.assertRaises(DataQualityError):
                validate_bronze_manifest(manifest_path)


if __name__ == "__main__":
    unittest.main()
