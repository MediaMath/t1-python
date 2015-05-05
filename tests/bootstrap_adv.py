#!/usr/bin/env python

from datetime import datetime, timedelta
import terminalone
from terminalone.utils import credentials


def edit_name(name):
	if not name:
		return
	last_char = name[-1]
	if not last_char.isdigit():
		if last_char != ' ':
			return name + ' 1'
		return name + '1'
	return name[:-1] + str(int(last_char)+1)


now = datetime.now()
start_date, end_date = now + timedelta(days=1), now + timedelta(days=8)

campaigns = [
	{
		'name': 'Main Campaign',
		'status': False,
		'start_date': start_date,
		'end_date': end_date,
		'frequency_type': 'no-limit',
		'advertiser_id': 100000,
		'goal_category': 'audience',
		'goal_type': 'cpa',
		'goal_value': 1.00,
		'margin_pct': 0.00,
		'merit_pixel_id': TODO,
		'spend_cap_amount': 1.00,
		'spend_cap_enabled': True,
		'total_budget': 1.00,
	},
]
strategies = [
	{
		'name': 'RTB Test Strategy'
	},
	{},
]
pixels = [
	{
		'name': 'Test Event Pixel',
		'advertiser_id': 100000,
		'eligible': True,
		'pixel_type': 'event',
		'status': True,
		'tag_type': 'js',
	},
	{
		'name': 'Test Data Pixel',
		'agency_id': 100000,
		'provider_id': 100,
		'cost_cpm': 0.00,
		'cost_cpts': 0.00,
		'cost_pct_cpm': 0.00,
		'eligible': True,
		'pixel_type': 'data',
		'pricing': 'CPM',
		'tag_type': 'image',
	}
]
concepts = [
	{
		'name': 'Test Concept',
		'advertiser_id': 100000,
		'status': True,
	}
]
