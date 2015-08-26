#!/usr/bin/env python

from datetime import datetime, timedelta
import json
import logging
import sys
from terminalone import T1
from terminalone.utils import credentials

if sys.version_info.major > 2:
    PY3 = True
else:
    PY3 = False


def iteritems(d):
    if PY3:
        return d.items()
    return d.iteritems()


def edit_name(name):
    if not name:
        return
    last_char = name[-1]
    if not last_char.isdigit():
        if last_char != ' ':
            return name + ' 1'
        return name + '1'
    return name[:-1] + str(int(last_char) + 1)


def setup(credentials):
    return T1(auth_method='cookie', **credentials)


now = datetime.now()

learned_vars = {
    'advertiser_id': None,
    'agency_id': None,
    'campaign_id': None,
    'provider_id': None,
    'concept_id': None,
}

campaigns = (
    [
        {
            'name': 'Main Campaign',
            'status': False,
            'use_default_ad_server': True,
            'ad_server_id': 9,
            'advertiser_id': None,
            'currency_code': 'USD',
            'start_date': now + timedelta(days=30),
            'end_date': now + timedelta(days=60),
            'frequency_type': 'no-limit',
            'goal_category': 'audience',
            'goal_type': 'spend',
            'goal_value': 1.00,
            'margin_pct': 0.00,
            'service_type': 'SELF',
            'total_budget': 1.00,
        },
    ], 'campaigns', 'campaign_id',
)
strategies = (
    [
        {
            'name': 'RTB Test Strategy',
            'budget': 1.00,
            'campaign_id': None,
            'use_campaign_start': True,
            'use_campaign_end': True,
            'frequency_type': 'no-limit',
            'goal_type': 'spend',
            'max_bid': 1.00,
            'pacing_amount': 1.00,
            'pacing_interval': 'day',
            'pacing_type': 'even',
            'status': False,
            'type': 'REM',

        },
    ], 'strategies', None,
)
pixels = (
    [
        {
            'name': 'Test Event Pixel',
            'advertiser_id': None,
            'eligible': True,
            'pixel_type': 'event',
            'status': True,
            'tag_type': 'js',
        },
        {
            'name': 'Test Data Pixel',
            'agency_id': None,
            'provider_id': None,
            'cost_cpm': 0.00,
            'cost_cpts': 0.00,
            'cost_pct_cpm': 0.00,
            'eligible': True,
            'pixel_type': 'data',
            'pricing': 'CPM',
            'tag_type': 'image',
        }
    ], 'pixel_bundles', None,
)
concepts = (
    [
        {
            'name': 'AdAge',
            'advertiser_id': None,
            'status': True,
        }
    ], 'concepts', 'concept_id',
)
creatives = (
    [
        {
            'name': 'AdAge 300x250',
            'advertiser_id': None,
            'ad_server_type': 'OTHER',
            'concept_id': None,
            'external_identifier': '1',
            'height': 1,
            'width': 1,
            'status': True,
            'tag': '<script type="text/javascript"></script>',
            'tag_type': 'SCRIPT',
            'tpas_ad_tag_name': 'not-applicable',
        }
    ], 'atomic_creatives', None,
)

# Need to iterate in a certain order. campaign needs to be created before
# strategy is created, for instance, so that we can fill in campaign_id
order = [
    campaigns,
    strategies,
    concepts,
    creatives,
    pixels,
]


def learn_props(props):
    for key, value in iteritems(props):
        if value is None and key in learned_vars:
            props[key] = learned_vars[key]


def bootstrap_advertiser(t1):
    for item in order:
        items, count = t1.get(item[1], count=True)
        if count < len(item[0]):
            for propset in item[0]:
                learn_props(propset)
                i = t1.new(item[1], properties=propset)
                i.save()
                if item[2] is not None:
                    learned_vars[item[2]] = i.id
        else:
            if item[2] is not None:
                learned_vars[item[2]] = next(items).id


def load_defaults(filename):
    with open(filename) as f:
        data = json.load(f)
    learned_vars.update(data)


def main():
    t1 = setup(credentials())
    load_defaults('defaults.json')
    bootstrap_advertiser(t1)


if __name__ == '__main__':
    import argparse

    __parser = argparse.ArgumentParser(description='bootstrap helper')
    __parser.add_argument('-v', '--verbose', action='store_true', help='debug logging')
    args = __parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    main()
