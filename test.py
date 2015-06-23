from __future__ import print_function
from terminalone import T1, filters
from terminalone.utils import credentials
from terminalone.vendor.six import six

REPORTS = []

# TODO make real unit tests out of this

def setup(credentials):
	try:
		t1 = T1(auth_method='cookie',
				**credentials)
	except Exception as e:
		print(e.message)
		print(dir(e))
		# print(t1.response)
		raise

	assert hasattr(t1, 'user_id'), 'No user ID present'
	return t1

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
	adv = t1.get('advertisers', 105162)
	assert adv.id == 105162, "Expected ID 105162, got: %d" % adv.id
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
	pxl = next(t1.get('pixel_bundles', limit={'advertiser': 105162},
		full='pixel_bundle', page_limit=1))
	assert pxl.advertiser_id == 105162, 'Expected adv ID 105162, got: %d' % pxl.advertiser_id

	pxl = next(t1.get('pixel_bundles', limit={'agency.organization': 100001},
		full='pixel_bundle', page_limit=1))
	assert pxl.pixel_type != 'event', 'Expected non-event pixel, got: %r' % pxl.pixel_type

def test_include(t1):
	pxl = next(t1.get('pixel_bundles', limit={'advertiser': 105162},
	assert hasattr(pxl, 'advertiser'), 'Expected advertiser included, got: %r' % pxl
	assert hasattr(pxl.advertiser, 'id'), 'Expected advertiser instance, got: %r' % pxl.advertiser

def test_find(t1):
	pxls = t1.find('pixel_bundles', 'id', operator=filters.IN,
		candidates=[452050, 452051, 452052])
	count = len(list(pxls))
	assert count == 3, 'Expected 3 entities, got: %d' % count

	camps = t1.find('campaigns', 'name', filters.CASE_INS_STRING,
		'test*', page_limit=5)
	names = [c.name for c in camps]
	good = all(n.lower().startswith('test') for n in names)
	assert good, 'Expected all results to start with "test", got: %r' % names

def test_permissions(t1):
	p = t1.get('users', 1090, child='permissions')
	assert p._type == 'permission', 'Expected permission entity, got: %r' % p

def test_picard_meta(t1):
	r = t1.new('report')
	md = r.metadata
	assert hasattr(md, 'keys'), 'Expected mapping structure, got: %r' % type(md)

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


def main():
	tests = [
		test_collection,
		test_counts,
		test_get_all,
		test_entity_get_save,
		test_full,
		test_limit,
		test_include,
		test_find,
		test_permissions,
		test_picard_meta,
		test_report_meta,
	]

	t1 = setup(credentials())
	for test in tests:
		test(t1)
		print("Passed test for {}".format(test.__name__.replace('test_', '')))
	else:
		print("Passed all tests!")

if __name__ == '__main__':
	main()
