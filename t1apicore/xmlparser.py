# -*- coding: utf-8 -*-
"""Parses XML output from T1 and returns a sane Python object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

# myobject = {
# 	'entity_count': 594,
# 	'entities': self.entities,
# 	'status_code': self.status_code
# }

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET
import t1error

class T1XMLParser(object):
	"""docstring for T1XMLParser"""
	def __init__(self, response):
		# super(T1XMLParser, self).__init__()
		# self.response = response
		self.result = ET.parse(response)
		self.status_code = self.get_status(self.result)
		if self.result.find('entities') is not None:
			self.entity_count = int(self.result.find('entities').get('count'))
			self.entities = map(self.dictify_entity, self.result.iter('entity'))
		elif self.result.find('entity') is not None:
			self.entity_count = 1
			self.entities = map(self.dictify_entity, self.result.iter('entity'))
		# return self.entities
		self.attribs = {'entity_count': self.entity_count, 'entities': self.entities,
						'status_code': self.status_code}
		pass
	
	def get_status(self, xmlresult, error=False):
		"""Uses a simple ET method to get the status code of T1 XML response.
		
		If the code is valid, returns True; otherwise raises the appropriate T1 Error.
		"""
		status_code = xmlresult.find('status').get('code')
		message = xmlresult.find('status').text
		if status_code == 'ok':
			return True # Assumes using self.status_code = self.get_status(result)
		elif status_code == 'auth_required':
			self.status_code = False
			raise t1error.T1Error(status_code, 'Authentication required')
		elif status_code == 'invalid':
			# Aggregate all the errors, then raise T1Exception/T1Error
			pass
		elif status_code == 'not_found':
			self.status_code = False
			raise t1error.T1NotFoundError(status_code, message)
		pass
	
	def dictify_entity(self, entity):
		output = entity.attrib
		for prop in list(entity):
			output[prop.attrib['name']] = prop.attrib['value']
		return output
	pass

def T1RawParse(response):
	"""Raw access to ET parsing.
	
	Mainly used for T1 Connection objects to access cElementTree without directly
	importing it. This lets All the XML parsing happen here, while the rest of the 
	library can use it freely.
	"""
	return ET.parse(response)
