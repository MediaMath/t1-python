# -*- coding: utf-8 -*-
"""Provides permission object."""

from __future__ import absolute_import
from ..errors import ClientError
from ..entity import SubEntity


class Permission(SubEntity):
    """docstring for Permission."""
    collection = 'permissions'
    resource = 'permission'
    _relations = {
    }

    _pull = {
        '_type': None,
        'advertiser': None,
        'agency': None,
        'organization': None,
        'edit_data_definition': int,
        'view_data_definition': int,
        'edit_segments': int,
        'edit_campaigns': int,
        'access_internal_fees': int,
        'edit_margins_and_performance': int,
        'view_organizations': int,
        'view_segments': int,
        'view_dmp_reports': int,
        'type': None,
        'role': None,
        'scope': None,
    }
    _push = {
        'advertiser_id': None,
        'agency_id': None,
        'organization_id': None,
        }

    def __init__(self, session, properties=None, **kwargs):
        super(Permission, self).__init__(session, properties, **kwargs)

    def _change_access(self, entity_access, entity_id, add):
        if entity_access not in ['advertiser', 'agency', 'organization']:
            raise ClientError('Must be one of advertiser, agency, organization!')
        if add:
            placeholder_name = 'Placeholder for {} {} access'.format(entity_access, entity_id)
            if self.properties[entity_access] is None:
                self.properties[entity_access] = {}
            self.properties[entity_access][entity_id] = placeholder_name
        else:
            self.properties[entity_access].pop(entity_id)

    def add_access(self, entity_access, entity_id):
        self._change_access(entity_access, entity_id, True)

    def remove_access(self, entity_access, entity_id):
        self._change_access(entity_access, entity_id, False)

    def save(self, data=None, url=None):
        """Extra validation for data pixels

        :param data: dict optional data to use instead of self
        :return: None. Object is updated or error is raised
        """

        if data is None:
            data = self.properties.copy()
        data.pop('organization', None)
        data.pop('agency', None)
        data.pop('advertiser', None)

        if self.properties['advertiser'] is not None:
            data['advertiser_id'] = self.properties['advertiser'].keys()
        if self.properties['agency'] is not None:
            data['agency_id'] = self.properties['agency'].keys()
        if self.properties['organization'] is not None:
            data['organization_id'] = self.properties['organization'].keys()
        print data
        return super(Permission, self).save(data=data, url=url)
