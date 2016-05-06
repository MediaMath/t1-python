from __future__ import absolute_import
import unittest
import responses
import requests
from .requests_patch import patched_extract_cookies_to_jar
from terminalone import T1, filters

mock_credentials = {
    'username': 'user',
    'password': 'password',
    'api_key': 'api_key',
}

API_BASE = 'api.mediamath.com'

requests.sessions.extract_cookies_to_jar = patched_extract_cookies_to_jar
requests.adapters.extract_cookies_to_jar = patched_extract_cookies_to_jar


class TestGets(unittest.TestCase):
    @responses.activate
    def setUp(self):
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
    def test_get_strategy_day_parts(self):
        with open('tests/fixtures/strategy_day_parts.xml') as f:
            fixture = f.read()
        responses.add(responses.GET, 'https://api.mediamath.com/api/v2.0/strategies/941273/day_parts',
                      body=fixture,
                      content_type='application/xml')
        day_parts = self.t1.get('strategies', 941273, child='day_parts')

        c = 0
        for _ in day_parts:
            c += 1
        self.assertEqual(c, 3)

    @responses.activate
    def test_entity_get_save(self):
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
        with open('tests/fixtures/advertisers.xml') as f:
            advertisers = f.read()
        with open('tests/fixtures/advertisers_limit_1.xml') as f:
            advertiser = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/advertisers?'
                      'api_key=api_key&page_limit=1&page_offset=0&sort_by=id',
                      body=advertisers,
                      content_type='application/xml',
                      match_querystring=True)
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/advertisers?api_key='
                      'api_key&full=%2A&page_limit=1&page_offset=0&sort_by=id',
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
        with open('tests/fixtures/atomic_creatives_with_creative_approvals.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/atomic_creatives/1000'
                      '?api_key=api_key&with=creative_approvals',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)
        atomic = self.t1.get('atomic_creatives', 1000, include='creative_approvals')
        self.assertEqual(3, len(atomic.creative_approvals))

    @responses.activate
    def test_limit(self):
        with open('tests/fixtures/data_pixel_bundle_full.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/pixel_bundles/limit/'
                      'advertiser=29?api_key=api_key&full=pixel_bundle'
                      '&page_limit=1&page_offset=0&sort_by=id',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)

        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/pixel_bundles/limit/'
                      'agency.organization=100001?api_key=api_key&full='
                      'pixel_bundle&page_limit=1&page_offset=0&sort_by=id',
                      body=fixture,
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
        with open('tests/fixtures/pixel_bundle_with_advertiser.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/pixel_bundles/limit/'
                      'advertiser=29?api_key=api_key&with=advertiser&full=%2A'
                      '&page_limit=1&page_offset=0&sort_by=id',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)

        pxl = next(self.t1.get('pixel_bundles', limit={'advertiser': 29},
                               include='advertiser', full=True, page_limit=1))
        assert hasattr(pxl, 'advertiser'), 'Expected advertiser included, got: %r' % pxl
        assert hasattr(pxl.advertiser, 'id'), 'Expected advertiser instance, got: %r' % pxl.advertiser

    @responses.activate
    def test_include_traversals(self):
        with open('tests/fixtures/pixel_bundle_with_advertiser_agency.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/pixel_bundles/limit/'
                      'advertiser=29?api_key=api_key&with=advertiser%2Cagency'
                      '&full=%2A&page_limit=1&page_offset=0&sort_by=id',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)

        pxl = next(self.t1.get('pixel_bundles', limit={'advertiser': 29},
                               include=[['advertiser', 'agency'], ], full=True, page_limit=1))
        assert hasattr(pxl, 'advertiser'), 'Expected advertiser included, got: %r' % pxl
        assert hasattr(pxl.advertiser, 'agency'), 'Expected agency instance, got: %r' % pxl.advertiser

    @responses.activate
    def test_include_plural(self):
        with open('tests/fixtures/campaigns_with_strategies.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/campaigns/limit/'
                      'advertiser=29?api_key=api_key&page_limit=1'
                      '&with=strategies&page_offset=0&sort_by=id',
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
        with open('tests/fixtures/atomic_creatives_with_advertiser_concept.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/atomic_creatives/limit/'
                      'advertiser=29?api_key=api_key&with=advertiser&with=concept'
                      '&full=%2A&page_limit=1&page_offset=0&sort_by=-concept_id',
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
        with open('tests/fixtures/pixel_bundles.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/pixel_bundles'
                      '?api_key=api_key&q=%289991%2C9992%2C9993%29&page_limit='
                      '100&page_offset=0&sort_by=id',
                      body=fixture,
                      content_type='application/xml',
                      match_querystring=True)
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/campaigns'
                      '?api_key=api_key&q=name%3D%3Atest%2A&page_limit=5'
                      '&page_offset=0&sort_by=id',
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
    def test_picard_meta(self):
        with open('tests/fixtures/reports_meta.json') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/reporting/v1/std/meta'
                      '?api_key=api_key',
                      body=fixture,
                      content_type='application/json',
                      match_querystring=True)
        r = self.t1.new('report')
        md = r.metadata
        assert hasattr(md, 'keys'), 'Expected mapping structure, got: %r' % type(md)
        assert 'reports' in md, 'Expected overall metadata, got: %r' % md

    @responses.activate
    def test_target_dimensions(self):
        with open('tests/fixtures/target_dimensions.xml') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/api/v2.0/strategies/151940/target_dimensions/7',
                      body=fixture,
                      content_type='application/xml')
        t = self.t1.get('strategies', 151940, child='region')
        assert t._type == 'target_dimension', 'Expected target_dimension entity, got: %r' % t

    @responses.activate
    def test_picard_report(self):
        with open('tests/fixtures/performance.csv', "rt") as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/reporting/v1/std/performance?'
                      'api_key=api_key&filter=organization_id%3D100048'
                      '&time_window=yesterday&time_rollup=all'
                      '&dimensions=campaign_name',
                      body=fixture,
                      content_type='text/csv; charset=UTF-8',
                      match_querystring=True)
        with open('tests/fixtures/reports_meta.json') as f:
            fixture = f.read()
        responses.add(responses.GET,
                      'https://api.mediamath.com/reporting/v1/std/meta'
                      '?api_key=api_key',
                      body=fixture,
                      content_type='application/json',
                      match_querystring=True)

        r = self.t1.new('report')
        report = self.t1.new("report", r.report_uri("performance"))
        report_opts = {
            'dimensions': ['campaign_name'],
            'filter': {'organization_id': 100048},
            'time_rollup': 'all',
            'time_window': 'yesterday',
            'precision': 2
        }
        report.set(report_opts)

        headers, data = report.get()

        assert 'start_date' in headers, 'expected start_date field in headers'
        for line in data:
            assert isinstance(line, (list, tuple)), 'expected a list'
