# -*- coding: utf-8 -*-
"""Provides strategy concept object."""

from __future__ import absolute_import
from ..entity import Entity

class StrategyConcept(Entity):
	"""docstring for StrategyConcept."""
	collection = 'strategy_concepts'
	type = 'strategy_concept'
	_relations = {
		'concept',
		'strategy',
	}
	_pull = {
		'concept_id': int,
		'id': int,
		'status': Entity._int_to_bool,
		'strategy_id': int,
		'version': int,
	}
	_push = _pull.copy()
	_push.update({
		'status': int,
	})
	def __init__(self, session, properties=None, **kwargs):
		super(Concept, self).__init__(session, properties, **kwargs)
