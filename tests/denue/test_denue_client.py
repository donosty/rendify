import unittest

from rendify.denue.client import build_buscar_area_act_url


class TestBuildBuscarAreaActUrl(unittest.TestCase):
    def test_build_cdmx_sample_url(self):
        url = build_buscar_area_act_url(
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
            token="TEST_TOKEN",
        )

        expected_url = (
            "https://www.inegi.org.mx/app/api/denue/v1/consulta/"
            "BuscarAreaAct/09/0/0/0/0/0/0/0/0/0/1/15/0/TEST_TOKEN"
        )

        self.assertEqual(url, expected_url)


if __name__ == "__main__":
    unittest.main()