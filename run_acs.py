# ! /usr/bin/env python

from __future__ import print_function

import random

from terminalone import T1, filters
from terminalone.utils import credentials
from terminalone.vendor import six
from terminalone.errors import AuthRequiredError
from dotenv import load_dotenv
import os


dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)

REPORTS = []
API_BASE = 'api.mediamath.com'


ADVERTISER_ID = int(os.environ.get('ACCEPTANCE_TEST_ADVERTISER'))
STRATEGY_ID = int(os.environ.get('ACCEPTANCE_TEST_STRATEGY'))


def setup_oauth(user_credentials, use_json):
    t1 = T1(auth_method='oauth2-resourceowner',
            api_base=API_BASE,
            json=use_json,
            environment='sandbox',
            **user_credentials)
    assert hasattr(t1, 'user_id'), 'No user ID present'
    return t1


def setup(user_credentials, use_json):
    t1 = T1(auth_method='cookie',
            api_base=API_BASE,
            json=use_json,
            **user_credentials)
    assert hasattr(t1, 'user_id'), 'No user ID present'
    return t1


def test_session_id(t1):
    t2 = T1(session_id=t1.session_id, api_base=API_BASE, auth_method='cookie')
    assert hasattr(t2, 'username'), 'Expected new T1 session, got: %r' % t2


def test_collection(t1):
    adv = t1.get('advertisers')
    advs = len(list(adv))
    assert advs == 100, "Expected 100 advertisers, got: %d" % advs


def test_counts(t1):
    a, num_advs = t1.get('advertisers', page_limit=1, count=True)
    assert num_advs > 100, 'Expected many advertisers, got: %d' % num_advs
    a = next(a)
    assert a._type == 'advertiser', 'Expected advertiser, got: %r' % a._type


def test_get_all(t1):
    orgs, count = t1.get('organizations', count=True, get_all=True)
    c = 0
    for org in orgs:
        c += 1
    assert c == count, 'Expected %d orgs, got %d' % (count, c)


def test_entity_get_save(t1):
    adv = t1.get('advertisers', ADVERTISER_ID)
    assert adv.id == ADVERTISER_ID, "Expected ID %d, got: %d" % (ADVERTISER_ID, adv.id)
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


def test_full(t1):
    adv = next(t1.get('advertisers', page_limit=1))
    assert not hasattr(adv, 'status'), 'Expected limited record, got: %r' % adv

    adv = next(t1.get('advertisers', page_limit=1, full=True))
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


def test_limit(t1):
    pxl = next(t1.get('pixel_bundles', limit={'advertiser': ADVERTISER_ID},
                      full='pixel_bundle', page_limit=1))
    assert pxl.advertiser_id == ADVERTISER_ID, 'Expected adv ID %d, got: %d' % (ADVERTISER_ID, pxl.advertiser_id)

    pxl = next(t1.get('pixel_bundles', limit={'agency.organization': 100048},
                      full='pixel_bundle', page_limit=1))
    assert pxl.pixel_type != 'event', 'Expected non-event pixel, got: %r' % pxl.pixel_type


def test_include(t1):
    pxl = next(t1.get('pixel_bundles', limit={'advertiser': ADVERTISER_ID},
                      include='advertiser', full=True, page_limit=1))
    assert hasattr(
        pxl, 'advertiser'), 'Expected advertiser included, got: %r' % pxl
    assert hasattr(
        pxl.advertiser, 'id'), 'Expected advertiser instance, got: %r' % pxl.advertiser


def test_include_traversal(t1):
    pxl = next(t1.get('pixel_bundles', limit={'advertiser': ADVERTISER_ID},
                      include=[['advertiser', 'agency'], ], full=True, page_limit=1))
    assert hasattr(
        pxl, 'advertiser'), 'Expected advertiser included, got: %r' % pxl
    assert hasattr(
        pxl.advertiser, 'agency'), 'Expected agency instance, got: %r' % pxl.advertiser


def test_include_plural(t1):
    camp = next(t1.get('campaigns', limit={'advertiser': ADVERTISER_ID},
                       include='strategies', page_limit=1))
    assert hasattr(
        camp, 'strategies'), 'Expected strategies included, got: %r' % camp
    assert isinstance(
        camp.strategies, list), 'Expected list of strategies, got: %r' % camp.strategies
    assert hasattr(camp.strategies[
                   0], 'id'), 'Expected strategy instances, got: %r' % camp.strategies[0]


def test_include_multi(t1):
    # sort_by=-concept_id to ensure that we get a creative with a concept
    ac = next(t1.get('atomic_creatives', limit={'advertiser': ADVERTISER_ID},
                     include=[['advertiser', ], ['concept', ]],
                     full=True,
                     page_limit=1,
                     sort_by='-concept_id'))
    assert hasattr(
        ac, 'advertiser'), 'Expected advertiser included, got: %r' % ac
    assert hasattr(ac, 'concept'), 'Expected concept included, got: %r' % ac


def test_find(t1):
    pxls = t1.find('pixel_bundles', 'id', operator=filters.IN,
                   candidates=[1197721, 1197722, 1197723])
    count = len(list(pxls))
    assert count == 3, 'Expected 3 entities, got: %d' % count

    camps = t1.find('campaigns', 'name', filters.CASE_INS_STRING,
                    'test*', page_limit=5)
    names = [c.name for c in camps]
    good = all(n.lower().startswith('test') for n in names)
    assert good, 'Expected all results to start with "test", got: %r' % names


def test_permissions(t1):
    p = t1.get('users', 20628, child='permissions')
    assert p._type == 'permission', 'Expected permission entity, got: %r' % p


def test_target_dimensions(t1):
    t = t1.get('strategies', STRATEGY_ID, child='region')
    assert t._type == 'target_dimension', 'Expected target_dimension entity, got: %r' % t


def test_budget_flights(t1):
    camps = t1.find('campaigns', 'name', filters.CASE_INS_STRING,
                    'test*', page_limit=5, include='budget_flights', full=True)
    c = next(camps)
    old_version = c.budget_flights[0].version
    c.budget_flights[0].total_budget = random.randint(1, 100)
    c.budget_flights[0].save()
    assert c.budget_flights[0].version == old_version + 1, 'expected version to increment'

    for b in c.budget_flights:
        b.total_budget = random.randint(1, 100)
    c.save_budget_flights()
    assert c.budget_flights[0].version == old_version + 2, 'expected version to increment'


def test_picard_meta(t1):
    r = t1.new('report')
    md = r.metadata
    assert hasattr(
        md, 'keys'), 'Expected mapping structure, got: %r' % type(md)

    assert 'reports' in md, 'Expected overall metadata, got: %r' % md

    for report in six.iterkeys(md['reports']):
        REPORTS.append(report)


def test_report_meta(t1):
    for report in REPORTS:
        r = t1.new('report', report)
        md = r.metadata
        good = all(
            attr in md for attr in
            ['Name', 'URI_Data', 'URI_Meta', 'structure']
        )
        assert good, 'Expected report metadata, got: %r' % md


def test_session_id_oauth(t1):
    assert hasattr(t1, 'username'), 'Expected new T1 session, got: %r' % t1


def test_oauth_token(t1):
    try:
        t1.get('campaigns')
    except AuthRequiredError as e:
        assert 'access token expired' in e.message


def main():
    tests = [
        test_session_id,
        test_budget_flights,
        test_collection,
        test_counts,
        test_get_all,
        test_entity_get_save,
        test_full,
        test_limit,
        test_include,
        test_include_traversal,
        test_include_plural,
        test_include_multi,
        test_find,
        test_target_dimensions,
        test_permissions,
        test_picard_meta,
        test_report_meta,
    ]

    oauth_tests = [
        test_session_id_oauth,
        test_oauth_token,
    ]

    t1 = setup(credentials(), False)
    print('running XML tests')
    for test in tests:
        test(t1)
        print("Passed test for {}".format(test.__name__.replace('test_', '')))
    print("Passed all XML tests!")

    t1 = setup(credentials(), True)

    print('running json tests')
    for test in tests:
        test(t1)
        print("Passed test for {}".format(test.__name__.replace('test_', '')))
    print("Passed all json tests!")

    t1 = setup_oauth(credentials(), True)

    print("running oauth tests")
    for test in oauth_tests:
        test(t1)
        print("Passed test for {}".format(test.__name__.replace('test_', '')))
    print("Passed all oauth tests!")


if __name__ == '__main__':
    main()
