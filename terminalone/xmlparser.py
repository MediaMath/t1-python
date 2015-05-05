# -*- coding: utf-8 -*-
"""Parses XML output from T1 and returns a (relatively) sane Python object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import absolute_import
try:
	from itertools import imap
	import xml.etree.cElementTree as ET
except ImportError: # Python 3
	imap = map
	import xml.etree.ElementTree as ET
from .errors import (T1Error, APIError, ClientError, ValidationError,
						AuthRequiredError, NotFoundError)

ParseError = ET.ParseError

# Map known status.code repsonses to Exceptions. 'ok' signifies no exception,
# so that is None. 'invalid' can have many errors and needs
# an additional level of parsing, while the others can be instantiated directly.
STATUS_CODES = {
	'ok': None,
	'invalid': True,
	'not_found': NotFoundError,
	'auth_required': AuthRequiredError,
	'auth_error': AuthRequiredError,
	'error': APIError,
	'bad_request': ClientError,
}

class XMLParser(object):
	"""docstring for T1XMLParser"""
	def __init__(self, response, iter_=False):
		response.encoding = 'utf-8'
		result = ET.fromstring(response.content)
		self.get_status(result)
		if iter_:
			map_ = imap
		else:
			map_ = map
		if result.find('entities') is not None:
			try:
				self.entity_count = int(result.find('entities').get('count'))
			except TypeError:
				self.entity_count = 0
			self.entities = map_(self.dictify_entity,
								result.iterfind('entities/entity'))
		elif result.find('entity') is not None:
			self.entity_count = 1
			self.entities = map_(self.dictify_entity,
								result.iterfind('entity'))
		elif result.find('include') or result.find('exclude') or result.find('enabled') is not None:
			exclude = map_(self.dictify_entity,
								result.iterfind('exclude/entities/entity'))
			include = map_(self.dictify_entity,
								result.iterfind('include/entities/entity'))
			self.entity_count = 1
			self.entities = [{
				'_type': 'target_dimension',
				'exclude': exclude,
				'include': include,
				'rels': {},
			}]
		elif result.find('permissions') is not None:
			advertiser = self.dictify_permission_entity(
				next(result.iterfind('permissions/entities/advertiser'), None))
			agency = self.dictify_permission_entity(
				next(result.iterfind('permissions/entities/agency'), None))
			organization = self.dictify_permission_entity(
				next(result.iterfind('permissions/entities/organization'), None))

			# flags will only ever have one instance. But the return expects
			# an iterator, so let's just make a list out of it
			self.entities = [self.dictify_permission_entity(
				next(result.iterfind('permissions/flags'), None)),]
			self.entity_count = 1
			self.entities[0].update({
				'_type': 'permission',
				'advertiser': advertiser,
				'agency': agency,
				'organization': organization,
				'rels': {},
			})

		elif result.find('log_entries') is not None:
			self.entity_count = 1
			self.entities = map_(self.dictify_history_entry,
								result.iterfind('log_entries/entry'))
		# self.attribs = {'entity_count': self.entity_count,
		# 				'entities': self.entities,}

	def get_status(self, xmlresult):
		"""Gets the status code of T1 XML response.

		If code is valid, returns None; otherwise raises the appropriate Error.
		"""
		status_code = xmlresult.find('status').attrib['code']
		message = xmlresult.find('status').text

		try:
			e = STATUS_CODES[status_code]
		except KeyError:
			self.status_code = False
			raise T1Error(status_code, message)

		if e is None:
			self.status_code = True
			return

		self.status_code = False
		if e is True:
			message = self._parse_field_error(xmlresult)
			e = ValidationError

		raise e(status_code, message)

	def _parse_field_error(self, xml):
		errors = {}
		for error in xml.iter('field-error'):
			attribs = error.attrib
			errors[attribs['name']] = {'code': attribs['code'],
										'error': attribs['error']}
		return errors

	def dictify_entity(self, entity):
		output = entity.attrib
		# Hold relation objects in specific dict. T1Service instantiates the
		# correct classes.
		output['rels'] = {}
		if 'type' in output:
			output['_type'] = output['type']
			del output['type']
		for prop in entity:
			if prop.tag == 'entity': # Get parent entities recursively
				output['rels'][prop.attrib['rel']] = self.dictify_entity(prop)
			else:
				output[prop.attrib['name']] = prop.attrib['value']
		return output

	def dictify_permission_entity(self, entity):
		if not entity:
			return
		output = {}
		if entity.tag == 'flags':
			for prop in entity:
				output[prop.attrib['type']] = prop.attrib['value']
		else:
			for prop in entity:
				output[int(prop.attrib['id'])] = prop.attrib['name']
		return output

	def dictify_history_entry(self, entry):
		output = entry.attrib
		fields = {}
		for field in entry:
			kind = field.attrib['name']
			if kind != 'last_modified':
				fields[kind] = {'old_value': field.attrib['old_value'],
								'new_value': field.attrib['new_value']}
		output['fields'] = fields
		return output


def T1RawParse(raw_response):
	"""Raw access to ET parsing.

	Argument should be a raw HTTP Response object -- from requests, this means
	if resp = requests.get(something, stream=True),
	argument should be resp.raw

	Mainly used for T1 Connection objects to access cElementTree without directly
	importing it. This lets all the XML parsing happen here, while the rest of
	the library can use it freely.
	"""
	return ET.parse(raw_response)
