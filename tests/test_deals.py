from __future__ import absolute_import
import unittest
import responses
import requests
from .requests_patch import patched_extract_cookies_to_jar
from terminalone import T1
from terminalone.models import deal

mock_credentials = {
    'username': 'user',
    'password': 'password',
    'api_key': 'api_key',
}

API_BASE = 'api.mediamath.com'

requests.sessions.extract_cookies_to_jar = patched_extract_cookies_to_jar
requests.adapters.extract_cookies_to_jar = patched_extract_cookies_to_jar


class TestDeals(unittest.TestCase):
    @responses.activate
    def setUp(self):
        """set up test fixtures"""
        with open('tests/fixtures/xml/session.xml') as f:
            fixture = f.read()
        responses.add(responses.POST, 'https://api.mediamath.com/api/v2.0/login',
                      body=fixture,
                      adding_headers={
                          'Set-Cookie': 'adama_session=1',
                      },
                      content_type='application/xml')

        self.t1 = T1(auth_method='cookie',
                     api_base=API_BASE,
                     **mock_credentials)

    @responses.activate
    def test_collection(self):
        with open('tests/fixtures/json/media_api_deal.json') as f:
            fixture = f.read()
        responses.add(responses.GET, 'https://api.mediamath.com/media/v1.0/deals/11111',
                      body=fixture,
                      content_type='application/json')
        deal = self.t1.get('deals', 11111)
        self.assertIsNone(deal.sub_supply_source_id)

    def test_generate_json(self):
        mock_deal_properties = {
            "data": {
                "supply_source_id": 4,
                "id": 11111,
                "name": "Test deal",
                "price": {
                    "value": "4.3200",
                    "currency_code": "EUR"
                },
                "created_on": "2016-11-16T11:31:53+00:00",
                "entity_type": "deal",
                "price_type": "FLOOR",
                "permissions": {
                    "all_organizations": False,
                    "organization_ids": [],
                    "agency_ids": [
                        1234,
                    ],
                    "advertiser_ids": [
                        12345,
                        123456
                    ]
                },
                "sub_supply_source_id": None,
                "end_datetime": "2999-12-31T00:00:00+00:00",
                "status": True,
                "deal_identifier": "Deal_identifier",
                "start_datetime": "2016-11-16T12:31:10+00:00",
                "owner": {
                    "id": 22222,
                    "type": "ADVERTISER"
                },
                "updated_on": "2016-11-16T11:31:53+00:00",
                "price_method": "CPM"
            },
            "meta": {
                "status": "ok"
            }
        }
        test_deal = deal.Deal(None, properties=mock_deal_properties)
        #data = test_deal._validate_write(test_deal.data)
