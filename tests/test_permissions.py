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
        with open('tests/fixtures/session.xml') as f:
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
    def test_get_permissions(self):
        self.setup()
        with open('tests/fixtures/permissions.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/users/10000/permissions',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)

        p = self.t1.get('users', 10000, child='permissions')
        assert p._type == 'permission', 'Expected permission entity, got: {}'.format(p._type)
        assert p.parent_id == 10000, 'Expected parent id to be 1000, got: {}'.format(p.parent_id)

    @responses.activate
    def test_remove_advertiser(self):
        self.setup()
        with open('tests/fixtures/permissions.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/users/10000/permissions',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)

        p = self.t1.get('users', 10000, child='permissions')
        remove_id = 6
        assert remove_id in p.advertiser.keys(), 'Expected advertiser {} to be in access flags'.format(remove_id)

        p.remove('advertiser', 6)
        assert remove_id not in p.advertiser.keys(), 'advertiser {} should have been removed but is still there'\
            .format(remove_id)

    @responses.activate
    def test_it_should_remove_child_advertisers_when_removing_agency(self):
        self.setup()
        with open('tests/fixtures/permissions.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/users/10000/permissions',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)

        p = self.t1.get('users', 10000, child='permissions')
        remove_ids = [6, 7]

        for ad_id in remove_ids:
            assert ad_id in p.advertiser.keys(), 'Expected advertiser {} to be in access flags'.format(ad_id)

        p.remove('agency', 3)
        for ad_id in remove_ids:
            assert ad_id not in p.advertiser.keys(), 'child advertiser {} should have been removed but is still there'\
                .format(ad_id)

    @responses.activate
    def test_it_should_remove_child_agencies_and_advertisers_when_removing_organization(self):
        self.setup()
        with open('tests/fixtures/permissions.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/users/10000/permissions',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)

        p = self.t1.get('users', 10000, child='permissions')
        remove_advertiser_ids = [8, 9, 10]
        remove_agency_ids = [4, 5]
        for advertiser_id in remove_advertiser_ids:
            assert advertiser_id in p.advertiser.keys(), 'Expected advertiser {} to be in access flags'.format(advertiser_id)
        for agency_id in remove_agency_ids:
            assert agency_id in p.agency.keys(), 'Expected agency {} to be in access flags'.format(agency_id)

        p.remove('organization', 2)
        for advertiser_id in remove_advertiser_ids:
            assert advertiser_id not in p.advertiser.keys(), 'child advertiser {} should have been removed but is still there'\
                .format(advertiser_id)

        for agency_id in remove_agency_ids:
            assert agency_id not in p.agency.keys(), 'child agency {} should have been removed but is still there'\
                .format(agency_id)

    @responses.activate
    def test_it_should_add_entity_ids_on_save(self):
        self.setup()
        with open('tests/fixtures/permissions.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/users/10000/permissions',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)

        p = self.t1.get('users', 10000, child='permissions')
        p.add('organization', 10)
        data = p._generate_save_data()
        assert sorted(data['organization_id']) == [1, 2, 10], data['organization_id']

    @responses.activate
    def test_it_should_add_access_to_empty_permissions(self):
        self.setup()
        with open('tests/fixtures/permissions_none.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/users/10000/permissions',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)

        p = self.t1.get('users', 10000, child='permissions')
        p.add('organization', 10)
        data = p._generate_save_data()
        assert sorted(data['organization_id']) == [10], data['organization_id']
