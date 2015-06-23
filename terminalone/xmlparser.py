# -*- coding: utf-8 -*-
"""Parses XML output from T1 and returns a (relatively) sane Python object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import absolute_import
try:
	from itertools import imap
	map = imap
	import xml.etree.cElementTree as ET
except ImportError: # Python 3
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
	def __init__(self, response):
		response.encoding = 'utf-8'
		result = ET.fromstring(response.content)
		self.get_status(result, response)

		xfind = lambda haystack, needle: haystack.find(needle) is not None

		if xfind(result, 'entities'):
			self._parse_collection(result)

		elif xfind(result, 'entity'):
			self.entity_count = 1
			self.entities = self._parse_entities(result)

		elif any(xfind(result, x) for x in ['include, exclude', 'enabled']):
			self._parse_target_dimensions(result)

		elif xfind(result, 'permissions'):
			self._parse_permissions(result)

		elif xfind(result, 'log_entries'):
			self.entity_count = 1
			self.entities = map(self.dictify_history_entry,
								result.iterfind('log_entries/entry'))

	def get_status(self, xmlresult, response):
		"""Gets the status code of T1 XML response.

		If code is valid, returns None; otherwise raises the appropriate Error.
		"""
		status = xmlresult.find('status')
		if status is None:
			raise T1Error(None, response.content)
		status_code = status.attrib['code']
		message = status.text

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

	def _parse_entities(self, ent_root):
		return map(self.dictify_entity, ent_root.iterfind('entity'))

	def _parse_collection(self, result):
		root = result.find('entities')
		self.entity_count = int(root.get('count') or 0)
		self.entities = self._parse_entities(root)

	def _parse_target_dimensions(self, result):
		exclude = map(self.dictify_entity,
					  result.iterfind('exclude/entities/entity'))
		include = map(self.dictify_entity,
					  result.iterfind('include/entities/entity'))
		self.entity_count = 1
		self.entities = [{
			'_type': 'target_dimension',
			'exclude': exclude,
			'include': include,
		}]

	def _parse_permissions(self, result):
		root = result.find('permissions/entities')
		organization, agency, advertiser = None, None, None
		if root:
			advertiser = self.dictify_permission(root.find('advertiser'))
			agency = self.dictify_permission(root.find('agency'))
			organization = self.dictify_permission(root.find('organization'))

		flags = self.dictify_permission(result.find('permissions/flags'))
		flags.update({
			'_type': 'permission',
			'advertiser': advertiser,
			'agency': agency,
			'organization': organization,
		})

		# There will only be one instance here.
		# But the caller expects an iterator, so make a list of it
		self.entities, self.entity_count = [flags,], 1

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
		output['relations'] = {}
		if 'type' in output:
			output['_type'] = output['type']
			del output['type']
		for prop in entity:
			if prop.tag == 'entity': # Get parent entities recursively
				ent = self.dictify_entity(prop)
				if prop.attrib['rel'] == ent.get('_type'):
					output['relations'][prop.attrib['rel']] = ent
				else:
					output['relations'].setdefault(prop.attrib['rel'], []).append(ent)
			else:
				output[prop.attrib['name']] = prop.attrib['value']
		return output

	def dictify_permission(self, entity):
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
