from __future__ import absolute_import
import unittest
import responses
import requests
from .requests_patch import patched_extract_cookies_to_jar
from terminalone import T1

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

    @responses.activate
    def test_generate_json(self):

        with open('tests/fixtures/json/media_api_deal.json') as f:
            fixture = f.read()
        responses.add(responses.GET, 'https://api.mediamath.com/media/v1.0/deals/11111',
                      body=fixture,
                      content_type='application/json')
        test_deal = self.t1.get('deals', 11111)
        data = test_deal._validate_json_post(test_deal._init_properties)
        self.assertEqual(data.get('start_datetime'), "2016-11-16T12:31:10+0000")

    @responses.activate
    def test_strategy_with_deals(self):
        with open('tests/fixtures/json/strategy_with_deals.json') as f:
            fixture = f.read()
        responses.add(responses.GET, 'https://api.mediamath.com/api/v2.0/strategies/11111/deals',
                      body=fixture,
                      content_type='application/json')
        strategy = self.t1.get('strategies', 11111, child='deals')
        self.assertEqual(11111, strategy.deals[0].id)
        self.assertEqual(22222, strategy.deals[1].id)

    @responses.activate
    def test_strategy_with_deals_xml(self):
        with open('tests/fixtures/xml/strategy_with_deals.xml') as f:
            fixture = f.read()
        responses.add(responses.GET, 'https://api.mediamath.com/api/v2.0/strategies/11111/deals',
                      body=fixture,
                      content_type='application/xml')
        strategy = self.t1.get('strategies', 11111, child='deals')
        self.assertEqual(11111, strategy.deals[0].id)
        self.assertEqual(22222, strategy.deals[1].id)
