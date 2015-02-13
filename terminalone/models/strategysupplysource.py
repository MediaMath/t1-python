# -*- coding: utf-8 -*-
"""Provides strategy supply source object."""

from __future__ import absolute_import
from ..entity import Entity

class StrategySupplySource(Entity):
	"""docstring for StrategySupplySource."""
	collection = 'strategy_supply_sources'
	type = 'strategy_supply_sources'
	_relations = {
		'strategy',
		'supply_source',
	}
	_pull = {
		'id': int,
		'strategy_id': int,
		'supply_source_id': int,
		'version': int,
	}
	_push = _pull
	_readonly = Entity._readonly
	def __init__(self, session, properties=None, **kwargs):
		super(StrategySupplySource, self).__init__(session, properties, **kwargs)
