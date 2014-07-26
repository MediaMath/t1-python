# -*- coding: utf-8 -*-
"""Parses XML output from T1 and returns a (relatively) sane Python object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

# myobject = {
# 	'entity_count': 594,
# 	'entities': self.entities,
# 	'status_code': self.status_code
# }
# history:
# entities = [
# {
# 	'action': 'add', 'date': '2013-02-21T14:58:28', 'user_id': '2178', 'user_name': 'dblacklock@mediamath.com', 'fields':
# 	{
# 		'concept_id': {'old_value': 21, 'new_value': 31},
# 		'click_url': {'old_value': 'http://google.com', 'new_value': 'www.mediamath.com'}
# 	}
# }
# ]

try:
	from itertools import imap
	import xml.etree.cElementTree as ET
except ImportError: # Python 3
	imap = map
	import xml.etree.ElementTree as ET
from .t1error import *

class T1XMLParser(object):
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
			self.entity_count = int(result.find('entities').get('count'))
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
				'rels': {}
			}]
		elif result.find('log_entries') is not None:
			self.entity_count = 1
			self.entities = map_(self.dictify_history_entry,
								result.iterfind('log_entries/entry'))
		# self.attribs = {'entity_count': self.entity_count,
		# 				'entities': self.entities,}
	
	def get_status(self, xmlresult, error=False):
		"""Uses a simple ET method to get the status code of T1 XML response.
		
		If code is valid, returns True; otherwise raises the appropriate T1 Error.
		"""
		status_code = xmlresult.find('status').attrib['code']
		message = xmlresult.find('status').text
		if status_code == 'ok':
			return
		elif status_code == 'invalid':
			errors = {}
			for error in xmlresult.iter('field-error'):
				attribs = error.attrib
				errors[attribs['name']] = {'code': attribs['code'],
											'error': attribs['error']}
			self.status_code = False
			raise T1ValidationError(status_code, errors)
		elif status_code == 'not_found':
			self.status_code = False
			raise T1NotFoundError(status_code, message)
		elif status_code == 'auth_required':
			self.status_code = False
			raise T1AuthRequiredError(status_code, message)
		pass
	
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
