from __future__ import print_function
from __future__ import absolute_import

import unittest
import responses
import requests
from .requests_patch import patched_extract_cookies_to_jar

from terminalone import T1

mock_credentials = {
    'username': 'user;',
    'password': 'password',
    'api_key': 'api_key',
}

API_BASE = 'api.mediamath.com'

requests.sessions.extract_cookies_to_jar = patched_extract_cookies_to_jar
requests.adapters.extract_cookies_to_jar = patched_extract_cookies_to_jar


class TestPermissions(unittest.TestCase):
    def setup(self):
        """set up test fixtures"""
        with open('tests/fixtures/json/session.json') as f:
            fixture = f.read()
        responses.add(responses.POST, 'https://api.mediamath.com/api/v2.0/login',
                      body=fixture,
                      adding_headers={
                          'Set-Cookie': 'adama_session=1',
                      },
                      content_type='application/json')

        self.t1 = T1(auth_method='cookie',
                     api_base=API_BASE,
                     json=True,
                     **mock_credentials)

    @responses.activate
    def test_get_retired_audience_segments(self):
        self.setup()
        with open('tests/fixtures/json/retired_audience_segments.json') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/strategies/12345/retired_audience_segments',
                      body=fixture,
                      content_type='application/json')

        segments = self.t1.get('strategies', 12345, child='retired_audience_segments')
        retired_strategy = segments.next()
        retired_audience = retired_strategy.retired_audience_segment
        self.assertEqual(retired_audience.name, "Segment Name")
