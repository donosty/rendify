import unittest

from rendify.denue.client import build_buscar_area_act_url


class TestBuildBuscarAreaActUrl(unittest.TestCase):
    def build_url(
        self,
        establishment_name="0",
        record_start=1,
        record_end=15,
        token="TEST_TOKEN",
    ):
        """Build a URL using the standard CDMX sample parameters."""
        return build_buscar_area_act_url(
            entity="09",
            municipality="0",
            locality="0",
            ageb="0",
            block="0",
            sector="0",
            subsector="0",
            branch="0",
            class_code="0",
            establishment_name=establishment_name,
            record_start=record_start,
            record_end=record_end,
            establishment_id="0",
            token=token,
        )

    def test_builds_cdmx_sample_url(self):
        url = self.build_url()

        expected_url = (
            "https://www.inegi.org.mx/app/api/denue/v1/consulta/"
            "BuscarAreaAct/09/0/0/0/0/0/0/0/0/0/1/15/0/TEST_TOKEN"
        )

        self.assertEqual(url, expected_url)

    def test_encodes_spaces_and_accents(self):
        url = self.build_url(establishment_name="Café Central")

        expected_url = (
            "https://www.inegi.org.mx/app/api/denue/v1/consulta/"
            "BuscarAreaAct/09/0/0/0/0/0/0/0/0/"
            "Caf%C3%A9%20Central/1/15/0/TEST_TOKEN"
        )

        self.assertEqual(url, expected_url)

    def test_rejects_empty_token(self):
        with self.assertRaises(ValueError):
            self.build_url(token="")

    def test_rejects_whitespace_token(self):
        with self.assertRaises(ValueError):
            self.build_url(token="   ")

    def test_rejects_invalid_record_start(self):
        with self.assertRaises(ValueError):
            self.build_url(record_start=0)

    def test_rejects_record_end_before_start(self):
        with self.assertRaises(ValueError):
            self.build_url(record_start=20, record_end=10)


if __name__ == "__main__":
    unittest.main()