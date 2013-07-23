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
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET
from .t1error import *

class T1XMLParser(object):
	"""docstring for T1XMLParser"""
	def __init__(self, raw_response):
		result = ET.parse(raw_response)
		self.status_code = self.get_status(result)
		dictify_entity = self.dictify_entity
		xiter = result.iter
		if result.find('entities') is not None:
			self.entity_count = int(result.find('entities').get('count'))
			self.type = 'entities'
			self.entities = map(dictify_entity, xiter('entity'))
		elif result.find('entity') is not None:
			self.entity_count = 1
			self.type = 'entity'
			self.entities = map(dictify_entity, xiter('entity'))
		elif result.find('log_entries') is not None:
			self.type = 'history'
			self.entities = map(dictify_history_entry, xiter('entry'))
		# return self.entities
		self.attribs = {'entity_count': self.entity_count, 'entities': self.entities,
						'status_code': self.status_code, 'type': self.type}
		pass
	
	def get_status(self, xmlresult, error=False):
		"""Uses a simple ET method to get the status code of T1 XML response.
		
		If the code is valid, returns True; otherwise raises the appropriate T1 Error.
		"""
		status_code = xmlresult.find('status').attrib['code']
		message = xmlresult.find('status').text
		if status_code == 'ok':
			return True # Assumes using self.status_code = self.get_status(result)
		elif status_code == 'invalid':
			errors = {}
			for error in xmlresult.iter('field-error'):
				attribs = error.attrib
				errors[attribs['name']] = {'code': attribs['code'],
											'error': attribs['error']}
			self.status_code = False
			raise T1ValidationError(staus_code, errors)
		elif status_code == 'not_found':
			self.status_code = False
			raise T1NotFoundError(status_code, message)
		elif status_code == 'auth_required':
			self.status_code = False
			raise T1AuthRequiredError(status_code, message)
		pass
	
	def dictify_entity(self, entity):
		output = entity.attrib
		for prop in entity:
			output[prop.attrib['name']] = prop.attrib['value']
		return output
	
	def dictify_history_entry(self, entry):
		output = entry.attrib
		fields = {}
		for field in entry:
			if field.attrib['name'] != 'last_modified':
				fields[field.attrib['name']] = {'old_value': field.attrib['old_value'],
												'new_value': field.attrib['new_value']}
		output['fields'] = fields
		return output
		
	pass

def T1RawParse(raw_response):
	"""Raw access to ET parsing.
	
	Argument should be a raw HTTP Response object -- from requests, this means
	if resp = requests.get(something, stream=True),
	argument should be resp.raw
	
	Mainly used for T1 Connection objects to access cElementTree without directly
	importing it. This lets All the XML parsing happen here, while the rest of the 
	library can use it freely.
	"""
	return ET.parse(raw_response)
