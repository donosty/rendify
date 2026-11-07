
import os
import unittest
import json

from dotenv import load_dotenv

from rendify.denue.client import fetch_buscar_area_act


class TestDenueAPIIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()

        cls.token = os.getenv("DENUE_API_TOKEN")

        if not cls.token:
            raise unittest.SkipTest(
                "DENUE_API_TOKEN is not configured."
            )

    def test_fetches_cdmx_sample(self):
        response = fetch_buscar_area_act(
            entity="09",
            municipality="0",
            locality="0",
            ageb="0",
            block="0",
            sector="0",
            subsector="0",
            branch="0",
            class_code="0",
            establishment_name="0",
            record_start=1,
            record_end=15,
            establishment_id="0",
            token=self.token,
        )

        # Verify HTTP response metadata.
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "application/json",
            response.content_type.lower(),
        )

        # Verify original response preservation.
        self.assertIsInstance(response.raw_body, bytes)
        self.assertGreater(len(response.raw_body), 0)

        # Verify parsed records.
        records = response.records

        self.assertIsInstance(records, list)
        self.assertGreater(len(records), 0)

        self.assertTrue(
            all(isinstance(record, dict) for record in records)
        )

        # Verify that parsed records match the original JSON.
        original_records = json.loads(
            response.raw_body.decode("utf-8-sig")
        )

        self.assertEqual(records, original_records)

        # Inspect schema without printing establishment data.
        observed_fields = sorted({
            field
            for record in records
            for field in record
        })

        print(f"\nHTTP status: {response.status_code}")
        print(f"Records received: {len(records)}")
        print(f"Fields observed: {len(observed_fields)}")
        print("Fields:", ", ".join(observed_fields))


if __name__ == "__main__":
    unittest.main()
