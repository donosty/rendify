import os
import unittest

from dotenv import load_dotenv

from rendify.denue.client import fetch_buscar_area_act


class TestDenueAPIIntegration(unittest.TestCase):
    """Verify the complete DENUE request using a configured API token."""

    @classmethod
    def setUpClass(cls):
        """Load the local token and skip when integration access is unavailable."""
        load_dotenv()

        cls.token = os.getenv("DENUE_API_TOKEN")

        if not cls.token:
            raise unittest.SkipTest(
                "DENUE_API_TOKEN is not configured"
            )

    def test_fetches_cdmx_sample(self):
        """Fetch a small CDMX sample and inspect its returned record schema."""
        records = fetch_buscar_area_act(
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

        # Confirm both the collection type and the shape of every item.
        self.assertIsInstance(records, list)
        self.assertGreater(len(records), 0)
        self.assertTrue(
            all(isinstance(record, dict) for record in records)
        )

        first_record = records[0]

        print(f"\nRecords received: {len(records)}")

        # Print fields and representative types to document the live API schema.
        print("\nObserved fields:")
        print(", ".join(sorted({
            field
            for record in records
            for field in record
        })))

        print("\nRelevant field types:")

        candidate_fields = [
            "Id",
            "CLEE",
            "Nombre",
            "Clase_actividad",
            "Estrato",
            "AreaGeo",
            "Longitud",
            "Latitud",
            "Fecha_Alta",
        ]

        for field in candidate_fields:
            if field in first_record:
                
                value = first_record[field]
                print(
                    f"{field}: {type(value).__name__}"
                )
            else:
                print(f"{field}: absent")



        response = records.records
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.raw_body), 0)

        print(f"\nHTTP status: {response.status_code}")
        print(f"Content-Type: {response.content_type}")
        print(f"Records received: {len(records)}")


if __name__ == "__main__":
    unittest.main()
