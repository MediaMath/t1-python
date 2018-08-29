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


class TestBudgetFlights(unittest.TestCase):
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
    def test_get_single_budgetflight(self):
        with open('tests/fixtures/json/budgetflight_array_single.json') as f:
            fixture = f.read()
        responses.add(responses.GET, 'https://api.mediamath.com/api/v2.0/campaigns/11111/budget_flights',
                      body=fixture,
                      content_type='application/json')
        bfs, count = self.t1.get('campaigns', 11111, 'budget_flights', count=True)
        self.assertEqual(1, count)
        for bf in bfs:
            self.assertIsNotNone(bf.is_relevant)

    @responses.activate
    def test_get_multiple_budgetflight(self):
        with open('tests/fixtures/json/budgetflight_array_multiple.json') as f:
            fixture = f.read()
        responses.add(responses.GET, 'https://api.mediamath.com/api/v2.0/campaigns/22222/budget_flights',
                      body=fixture,
                      content_type='application/json')
        bfs, count = self.t1.get('campaigns', 22222, 'budget_flights', count=True)
        self.assertEqual(3, count)
        for bf in bfs:
            self.assertIsNotNone(bf.is_relevant)

    @responses.activate
    def test_save_single_budgetflight(self):
        with open('tests/fixtures/json/budgetflight_array_single.json') as f:
            fixture = f.read()
        with open('tests/fixtures/json/budgetflight_single.json') as f:
            singlefixture = f.read()
        responses.add(responses.GET, 'https://api.mediamath.com/api/v2.0/campaigns/11111/budget_flights',
                      body=fixture,
                      content_type='application/json')
        responses.add(responses.POST, 'https://api.mediamath.com/api/v2.0/campaigns/11111/budget_flights/12345',
                      body=singlefixture,
                      content_type='application/json')
        bfs = self.t1.get('campaigns', 11111, 'budget_flights')
        bf = next(bfs)
        bf.total_budget = 101
        bf.save()
        self.assertTrue('total_budget=101.0' in responses.calls[1].request.body)
        self.assertTrue('version=4' in responses.calls[1].request.body)
