import json
import unittest
from unittest.mock import patch

from rendify.denue.client import (
    DenueApiError,
    DenueAreaActivityQuery,
    build_buscar_area_act_url,
    fetch_page,
)


class TestDenueAreaActivityQuery(unittest.TestCase):
    def test_default_query_is_small_cdmx_sample(self):
        query = DenueAreaActivityQuery()
        query.validate()
        params = query.to_manifest_dict()
        self.assertEqual(params["entity_code"], "09")
        self.assertEqual(params["start_record"], 1)
        self.assertEqual(params["end_record"], 15)

    def test_url_contains_method_parameters_and_token(self):
        query = DenueAreaActivityQuery(class_code="722511")
        url = build_buscar_area_act_url(query, "test-token")
        self.assertIn("/BuscarAreaAct/09/0/0/0/0/0/0/0/722511/0/1/15/0/test-token", url)

    def test_invalid_scian_code_is_rejected(self):
        with self.assertRaises(ValueError):
            DenueAreaActivityQuery(class_code="123").validate()

    def test_invalid_record_range_is_rejected(self):
        with self.assertRaises(ValueError):
            DenueAreaActivityQuery(start_record=15, end_record=10).validate()

    def test_empty_token_is_rejected(self):
        with self.assertRaises(ValueError):
            build_buscar_area_act_url(DenueAreaActivityQuery(), "")

    @patch("rendify.denue.client.urlopen")
    def test_fetch_page_parses_json_list(self, mocked_urlopen):
        raw = json.dumps([{"Id": "123", "CLEE": "abc"}]).encode()
        response = unittest.mock.MagicMock()
        response.status = 200
        response.headers.get.return_value = "application/json"
        response.read.return_value = raw
        response.__enter__.return_value = response
        mocked_urlopen.return_value = response

        original, rows, status, content_type = fetch_page(
            DenueAreaActivityQuery(), "test-token"
        )
        self.assertEqual(original, raw)
        self.assertEqual(rows, [{"Id": "123", "CLEE": "abc"}])
        self.assertEqual(status, 200)
        self.assertEqual(content_type, "application/json")

    @patch("rendify.denue.client.urlopen")
    def test_fetch_page_rejects_unexpected_json_shape(self, mocked_urlopen):
        response = unittest.mock.MagicMock()
        response.status = 200
        response.headers.get.return_value = "application/json"
        response.read.return_value = b'{"error": "not a list"}'
        response.__enter__.return_value = response
        mocked_urlopen.return_value = response

        with self.assertRaises(DenueApiError):
            fetch_page(DenueAreaActivityQuery(), "test-token")


if __name__ == "__main__":
    unittest.main()
