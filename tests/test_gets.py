from __future__ import print_function
from __future__ import absolute_import

import unittest
import responses
import requests
from .requests_patch import patched_extract_cookies_to_jar

from terminalone import T1, filters

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
    def test_collection(self):
        self.setup()
        with open('tests/fixtures/advertisers.xml') as f:
            fixture = f.read()
        responses.add(responses.GET, 'https://api.mediamath.com/api/v2.0/advertisers',
                      body=fixture,
                      content_type='application/xml')
        advertisers = self.t1.get('advertisers')
        number_advertisers = len(list(advertisers))

        self.assertEqual(100, number_advertisers)

    @responses.activate
    def test_counts(self):
        self.setup()
        with open('tests/fixtures/advertisers.xml') as f:
            fixture = f.read()
        responses.add(responses.GET, 'https://api.mediamath.com/api/v2.0/advertisers',
                      body=fixture,
                      content_type='application/xml')
        advertisers, number_advertisers = self.t1.get('advertisers', page_limit=1, count=True)

        self.assertEqual(12345, number_advertisers)
        advertisers = next(advertisers)
        self.assertEqual(advertisers._type, 'advertiser', 'Expected advertiser, got: %r' % advertisers._type)

    @responses.activate
    def test_get_all(self):
        self.setup()
        with open('tests/fixtures/organizations.xml') as f:
            fixture = f.read()
        responses.add(responses.GET, 'https://api.mediamath.com/api/v2.0/organizations',
                      body=fixture,
                      content_type='application/xml')
        orgs, count = self.t1.get('organizations', count=True, get_all=True)
        c = 0
        for _ in orgs:
            c += 1
        self.assertEqual(c, count)

    @responses.activate
    def test_entity_get_save(self):
        self.setup()
        with open('tests/fixtures/advertiser.xml') as f:
            fixture = f.read()
        responses.add(responses.GET, 'https://api.mediamath.com/api/v2.0/advertisers/1',
                      body=fixture,
                      content_type='application/xml')
        responses.add(responses.POST, 'https://api.mediamath.com/api/v2.0/advertisers/1',
                      body=fixture,
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
        with open('tests/fixtures/advertisers.xml') as f:
            advertisers = f.read()
        with open('tests/fixtures/advertiser.xml') as f:
            advertiser = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/advertisers?page_limit=1&page_offset=0&sort_by=id',
                      body=advertisers,
                      content_type='application/xml',
                      match_querystring=True)
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/advertisers?full=%2A&page_limit=1&page_offset=0&sort_by=id',
                      body=advertiser,
                      content_type='application/xml',
                      match_querystring=True)

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

    @responses.activate
    def test_get_creative_approval(self):
        self.setup()
        with open('tests/fixtures/atomic_creatives_with_creative_approvals.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/atomic_creatives/1000?with=creative_approvals',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)
        atomic = self.t1.get('atomic_creatives', 1000, include='creative_approvals')
        self.assertEqual(3, len(atomic.creative_approvals))

    @responses.activate
    def test_limit(self):
        self.setup()
        with open('tests/fixtures/data_pixel_bundle_full.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/pixel_bundles/limit/advertiser=29'
                      '?full=pixel_bundle&page_limit=1&page_offset=0&sort_by=id',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)

        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/pixel_bundles/limit/agency.organization=100001'
                      '?full=pixel_bundle&page_limit=1&page_offset=0&sort_by=id',
                      body=open('tests/fixtures/data_pixel_bundle_full.xml').read(),
                      content_type='application/xml',
                      match_querystring=True)

        pxl = next(self.t1.get('pixel_bundles', limit={'advertiser': 29},
                               full='pixel_bundle', page_limit=1))
        self.assertEqual(29, pxl.advertiser_id)

        pxl = next(self.t1.get('pixel_bundles', limit={'agency.organization': 100001},
                               full='pixel_bundle', page_limit=1))
        self.assertNotEqual(pxl.pixel_type, 'event', 'Expected non-event pixel, got: %r' % pxl.pixel_type)

    @responses.activate
    def test_include(self):
        self.setup()
        with open('tests/fixtures/pixel_bundle_with_advertiser.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/pixel_bundles/limit/advertiser=29'
                      '?with=advertiser&full=%2A&page_limit=1&page_offset=0&sort_by=id',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)

        pxl = next(self.t1.get('pixel_bundles', limit={'advertiser': 29},
                               include='advertiser', full=True, page_limit=1))
        assert hasattr(pxl, 'advertiser'), 'Expected advertiser included, got: %r' % pxl
        assert hasattr(pxl.advertiser, 'id'), 'Expected advertiser instance, got: %r' % pxl.advertiser

    @responses.activate
    def test_include_traversals(self):
        self.setup()
        with open('tests/fixtures/pixel_bundle_with_advertiser_agency.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/pixel_bundles/limit/advertiser=29'
                      '?with=advertiser%2Cagency&full=%2A&page_limit=1&page_offset=0&sort_by=id',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)

        pxl = next(self.t1.get('pixel_bundles', limit={'advertiser': 29},
                               include=[['advertiser', 'agency'], ], full=True, page_limit=1))
        assert hasattr(pxl, 'advertiser'), 'Expected advertiser included, got: %r' % pxl
        assert hasattr(pxl.advertiser, 'agency'), 'Expected agency instance, got: %r' % pxl.advertiser

    @responses.activate
    def test_include_plural(self):
        self.setup()
        with open('tests/fixtures/campaigns_with_strategies.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/campaigns/limit/advertiser=29'
                      '?page_limit=1&with=strategies&page_offset=0&sort_by=id',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)

        camp = next(self.t1.get('campaigns', limit={'advertiser': 29},
                                include='strategies', page_limit=1))
        assert hasattr(camp, 'strategies'), 'Expected strategies included, got: %r' % camp
        assert isinstance(camp.strategies, list), 'Expected list of strategies, got: %r' % camp.strategies
        assert hasattr(camp.strategies[0], 'id'), 'Expected strategy instances, got: %r' % camp.strategies[0]

    @responses.activate
    def test_include_multi(self):
        self.setup()
        with open('tests/fixtures/atomic_creatives_with_advertiser_concept.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/atomic_creatives/limit/advertiser=29'
                      '?with=advertiser&with=concept&full=%2A&page_limit=1&page_offset=0&sort_by=-concept_id',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)
        ac = next(self.t1.get('atomic_creatives', limit={'advertiser': 29},
                              include=[['advertiser', ], ['concept', ]],
                              full=True,
                              page_limit=1,
                              sort_by='-concept_id'))
        assert hasattr(ac, 'advertiser'), 'Expected advertiser included, got: %r' % ac

    @responses.activate
    def test_find(self):
        self.setup()
        with open('tests/fixtures/pixel_bundles.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/pixel_bundles'
                      '?q=%289991%2C9992%2C9993%29&page_limit=100&page_offset=0&sort_by=id',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/campaigns'
                      '?q=name%3D%3Atest%2A&page_limit=5&page_offset=0&sort_by=id',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)

        pxls = self.t1.find('pixel_bundles', 'id', operator=filters.IN,
                            candidates=[9991, 9992, 9993])
        count = len(list(pxls))
        assert count == 3, 'Expected 3 entities, got: %d' % count

        camps = self.t1.find('campaigns', 'name', filters.CASE_INS_STRING,
                             'test*', page_limit=5)
        names = [c.name for c in camps]
        good = all(n.lower().startswith('pixel bundle') for n in names)
        assert good, 'Expected all results to start with "test", got: %r' % names

    @responses.activate
    def test_permissions(self):
        self.setup()
        with open('tests/fixtures/permissions.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/users/10000/permissions',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)

        p = self.t1.get('users', 10000, child='permissions')
        assert p._type == 'permission', 'Expected permission entity, got: %r' % p

    @responses.activate
    def test_picard_meta(self):
        self.setup()
        with open('tests/fixtures/reports_meta.json') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/reporting/v1/std/meta',
                      body=fixture,
                      content_type='application/json',
                      match_querystring=True)
        r = self.t1.new('report')
        md = r.metadata
        assert hasattr(md, 'keys'), 'Expected mapping structure, got: %r' % type(md)

        assert 'reports' in md, 'Expected overall metadata, got: %r' % md
