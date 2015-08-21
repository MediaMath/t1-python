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


class TestGets(unittest.TestCase):
    def setup(self):
        """set up test fixtures"""
        responses.add(responses.POST, 'https://api.mediamath.com/api/v2.0/login',
                      body=open('fixtures/session.xml').read(),
                      adding_headers={
                          'Set-Cookie': 'adama_session=1',
                      },
                      content_type='application/xml')

        self.t1 = T1(auth_method='cookie',
                     api_base=API_BASE,
                     **mock_credentials)

    @responses.activate
    def test_collection(self):
        self.setup()
        responses.add(responses.GET, 'https://api.mediamath.com/api/v2.0/advertisers',
                      body=open('fixtures/advertisers.xml').read(),
                      content_type='application/xml')
        advertisers = self.t1.get('advertisers')
        number_advertisers = len(list(advertisers))

        self.assertEqual(100, number_advertisers)

    @responses.activate
    def test_counts(self):
        self.setup()
        responses.add(responses.GET, 'https://api.mediamath.com/api/v2.0/advertisers',
                      body=open('fixtures/advertisers.xml').read(),
                      content_type='application/xml')
        advertisers, number_advertisers = self.t1.get('advertisers', page_limit=1, count=True)

        self.assertEqual(12345, number_advertisers)
        advertisers = next(advertisers)
        self.assertEqual(advertisers._type, 'advertiser', 'Expected advertiser, got: %r' % advertisers._type)

    @responses.activate
    def test_get_all(self):
        self.setup()
        responses.add(responses.GET, 'https://api.mediamath.com/api/v2.0/organizations',
                      body=open('fixtures/organizations.xml').read(),
                      content_type='application/xml')
        orgs, count = self.t1.get('organizations', count=True, get_all=True)
        c = 0
        for org in orgs:
            c += 1
        assert c == count, 'Expected %d orgs, got %d' % (count, c)

    @responses.activate
    def test_entity_get_save(self):
        self.setup()
        responses.add(responses.GET, 'https://api.mediamath.com/api/v2.0/advertisers/1',
                      body=open('fixtures/advertiser.xml').read(),
                      content_type='application/xml')
        responses.add(responses.POST, 'https://api.mediamath.com/api/v2.0/advertisers/1',
                      body=open('fixtures/advertiser.xml').read(),
                      content_type='application/xml')
        adv = self.t1.get('advertisers', 1)
        assert adv.id == 1, "Expected ID 1, got: %d" % adv.id
        assert all(
            hasattr(adv, item) for item in [
                'id',
                'name',
                'status',
                'agency_id',
                'created_on',
                'updated_on',
                'ad_server_id',
            ]
        ), 'Expected a full record, got: %r' % adv
        adv.save()

    @responses.activate
    def test_full(self):
        self.setup()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/advertisers?page_limit=1&page_offset=0&sort_by=id',
                      body=open('fixtures/advertisers.xml').read(),
                      content_type='application/xml',
                      match_querystring = True)
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/advertisers?full=%2A&page_limit=1&page_offset=0&sort_by=id',
                      body=open('fixtures/advertiser.xml').read(),
                      content_type='application/xml',
                      match_querystring = True)

        adv = next(self.t1.get('advertisers', page_limit=1))
        assert not hasattr(adv, 'status'), 'Expected limited record, got: %r' % adv

        adv = next(self.t1.get('advertisers', page_limit=1, full=True))
        assert all(
            hasattr(adv, item) for item in [
                'id',
                'name',
                'status',
                'agency_id',
                'created_on',
                'updated_on',
                'ad_server_id',
            ]
        ), 'Expected a full record, got: %r' % adv
