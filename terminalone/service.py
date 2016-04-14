# -*- coding: utf-8 -*-
"""Provides service object for T1."""

from __future__ import absolute_import, division
from itertools import chain
from types import GeneratorType
from .connection import Connection
from .entity import Entity
from .errors import ClientError
from .models import *
from .reports import Report
from .utils import filters
from .config import PATHS
from .vendor import six

CLASSES = {
    'ad_servers': AdServer,
    'advertisers': Advertiser,
    'agencies': Agency,
    'atomic_creatives': AtomicCreative,
    'audience_segments': AudienceSegment,
    'campaigns': Campaign,
    'concepts': Concept,
    'creative_approvals': CreativeApproval,
    'creatives': Creative,
    'deals': Deal,
    'organizations': Organization,
    'permissions': Permission,
    'pixel_bundles': PixelBundle,
    'pixel_providers': PixelProvider,
    'pixels': ChildPixel,
    'placement_slots': PlacementSlot,
    'publisher_sites': PublisherSite,
    'publishers': Publisher,
    'reports': Report,
    'rmx_strategies': RMXStrategy,
    'rmx_strategy_roi_target_pixels': RMXStrategyROITargetPixel,
    'seats': Seat,
    'site_lists': SiteList,
    'site_placements': SitePlacement,
    'strategies': Strategy,
    'strategy_audience_segments': StrategyAudienceSegment,
    'strategy_concepts': StrategyConcept,
    'strategy_day_parts': StrategyDayPart,
    'strategy_domain_restrictions': StrategyDomain,
    'strategy_supply_sources': StrategySupplySource,
    'supply_sources': SupplySource,
    'target_dimensions': TargetDimension,
    'target_values': TargetValue,
    'target_value_counts': TargetValue,
    'users': User,
    'vendor_contracts': VendorContract,
    'vendor_domains': VendorDomain,
    'vendor_pixel_domains': VendorPixelDomain,
    'vendor_pixels': VendorPixel,
    'vendors': Vendor,
    'verticals': Vertical,
}
MODEL_PATHS = {
    AdServer: 'ad_servers',
    Advertiser: 'advertisers',
    Agency: 'agencies',
    AtomicCreative: 'atomic_creatives',
    AudienceSegment: 'audience_segments',
    Campaign: 'campaigns',
    ChildPixel: 'pixels',
    Concept: 'concepts',
    Creative: 'creatives',
    CreativeApproval: 'atomic_creatives',
    Deal: 'deals',
    Organization: 'organizations',
    Permission: 'permissions',
    PixelBundle: 'pixel_bundles',
    PixelProvider: 'pixel_providers',
    PlacementSlot: 'placement_slots',
    Publisher: 'publishers',
    PublisherSite: 'publisher_sites',
    Report: 'reports',
    RMXStrategy: 'rmx_strategies',
    RMXStrategyROITargetPixel: 'rmx_strategy_roi_target_pixels',
    Seat: 'seats',
    SiteList: 'site_lists',
    SitePlacement: 'site_placements',
    Strategy: 'strategies',
    StrategyAudienceSegment: 'strategy_audience_segments',
    StrategyConcept: 'strategy_concepts',
    StrategyDayPart: 'strategy_day_parts',
    StrategyDomain: 'strategy_domain_restrictions',
    StrategySupplySource: 'strategy_supply_sources',
    SupplySource: 'supply_sources',
    TargetDimension: 'target_dimensions',
    TargetValue: 'target_values',
    User: 'users',
    Vendor: 'vendors',
    VendorContract: 'vendor_contracts',
    VendorDomain: 'vendor_domains',
    VendorPixel: 'vendor_pixels',
    VendorPixelDomain: 'vendor_pixel_domains',
    Vertical: 'verticals',
}
SINGULAR = {
    'ad_server': AdServer,
    'advertiser': Advertiser,
    'agency': Agency,
    'atomic_creative': AtomicCreative,
    'audience_segment': AudienceSegment,
    'campaign': Campaign,
    'concept': Concept,
    'creative': Creative,
    'creative_approval': CreativeApproval,
    'deal': Deal,
    'organization': Organization,
    'permission': Permission,
    'pixel': ChildPixel,
    'pixel_bundle': PixelBundle,
    'pixel_provider': PixelProvider,
    'placement_slot': PlacementSlot,
    'publisher': Publisher,
    'publisher_site': PublisherSite,
    'report': Report,
    'rmx_strategy': RMXStrategy,
    'rmx_strategy_roi_target_pixel': RMXStrategyROITargetPixel,
    'seat': Seat,
    'site_list': SiteList,
    'site_placement': SitePlacement,
    'strategy': Strategy,
    'strategy_audience_segment': StrategyAudienceSegment,
    'strategy_concept': StrategyConcept,
    'strategy_day_part': StrategyDayPart,
    'strategy_domain_restriction': StrategyDomain,
    'strategy_supply_source': StrategySupplySource,
    'supply_source': SupplySource,
    'target_dimension': TargetDimension,
    'target_value': TargetValue,
    'target_value_count': TargetValue,
    'user': User,
    'vendor': Vendor,
    'vendor_contract': VendorContract,
    'vendor_domain': VendorDomain,
    'vendor_pixel': VendorPixel,
    'vendor_pixel_domain': VendorPixelDomain,
    'vertical': Vertical,
}
CHILD_PATHS = {
    'acl': ('acl', 0),
    'audience_segments': ('audience_segments', 0),
    'audio': ('target_dimensions', 22),
    'browser': ('target_dimensions', 4),
    'channels': ('target_dimensions', 16),
    'concepts': ('concepts', 0),
    'connection speed': ('target_dimensions', 2),
    'content initiation': ('target_dimensions', 21),
    'country': ('target_dimensions', 14),
    'day_parts': ('day_parts', 0),
    'device': ('target_dimensions', 24),
    'dma': ('target_dimensions', 1),
    'fold position': ('target_dimensions', 19),
    'isp': ('target_dimensions', 3),
    'linear format': ('target_dimensions', 20),
    'mathselect250': ('target_dimensions', 8),
    'os': ('target_dimensions', 5),
    'permission': ('permissions', 0),
    'permissions': ('permissions', 0),
    'player size': ('target_dimensions', 23),
    'region': ('target_dimensions', 7),
    'safety': ('target_dimensions', 15),
    'supplies': ('supplies', 0),
}


class T1(Connection):
    """Service class for ALL other T1 entities, e.g.: t1 = T1(auth)

    Accepts authentication parameters. Supports get methods to get
    collections or an entity, find method to user inner-join-like queries.
    """

    def __init__(self,
                 username=None,
                 password=None,
                 api_key=None,
                 auth_method=None,
                 session_id=None,
                 environment='production',
                 api_base=None,
                 json=False,
                 **kwargs):
        """Set up session for main service object.

        :param username: str T1 Username
        :param password: str T1 Password
        :param api_key: str API Key approved in Developer Portal
        :param session_id: str API-provided prior session cookie.
            For instance, if you have a session ID provided by browser cookie,
            you can use that to authenticate a server-side connection.
        :param auth_method: enum('cookie', 'basic') Method for authentication.
        :param environment: str to look up API Base to use. e.g. 'production'
            for https://api.mediamath.com/api/v2.0
        :param api_base: str API base. should be in format https://[url] without
            trailing slash, and including version.
        """
        self.username = username
        self.password = password
        self.api_key = api_key
        self._authenticated = False
        self._auth = (self.username, self.password, self.api_key)
        self.environment = environment
        self.json = json
        super(T1, self).__init__(environment,
                                 api_base=api_base,
                                 json=json,
                                 **kwargs)
        if auth_method is not None:
            self.authenticate(auth_method, session_id=session_id, **kwargs)
        elif session_id is not None:
            self.authenticate('cookie', session_id=session_id, **kwargs)

    def _auth_cookie(self, session_id=None, **kwargs):
        """Authenticate using session cookie. If session ID is given, use that."""
        user = None
        if session_id is not None:
            # Set adama_session cookie
            from time import time
            self.session.cookies.set(
                name='adama_session',
                value=session_id,
                domain=self.api_base,
                expires=kwargs.get('expires', int(time() + 86400)),
            )
        else:
            user, _ = super(T1, self)._post(PATHS['mgmt'], 'login', data={
                'user': self.username,
                'password': self.password,
                'api_key': self.api_key,
            })

        self._check_session(user=user)
        self._authenticated = True

    def _auth_basic(self):
        """Authenticate using basic auth. DEPRECATED"""
        self.session.auth = ('{}|{}'.format(self.username, self.api_key),
                             self.password)
        self._check_session()
        self._authenticated = True

    def authenticate(self, auth_method, **kwargs):
        """Authenticate using method given."""
        if auth_method == 'cookie':
            return self._auth_cookie(**kwargs)
        elif auth_method == 'basic':
            return self._auth_basic()
        else:
            raise AttributeError('No authentication method for ' + auth_method)

    def new(self, collection, report=None, properties=None, *args, **kwargs):
        """Returns a fresh class instance for a new entity.

        ac = t1.new('atomic_creative') OR
        ac = t1.new('atomic_creatives') OR even
        ac = t1.new(terminalone.models.AtomicCreative)
        """
        if type(collection) == type and issubclass(collection, Entity):
            ret = collection
        elif '_acl' in collection:
            ret = ACL
        else:
            try:
                ret = SINGULAR[collection]
            except KeyError:
                ret = CLASSES[collection]

        if ret == Report:
            return ret(self.session,
                       report=report,
                       environment=self.environment,
                       api_base=self.api_base,
                       **kwargs)

        return ret(self.session,
                   environment=self.environment,
                   api_base=self.api_base,
                   properties=properties,
                   json=self.json,
                   *args, **kwargs)

    def _return_class(self, ent_dict,
                      child=None, child_id=None, entity_id=None, collection=None):
        """Generate item for new class instantiation"""
        ent_type = ent_dict.get('_type', ent_dict.get('type'))
        relations = ent_dict.get('relations')
        if child is not None:
            # Child can be either a target dimension (with an ID) or
            # a bare child, like concepts or permissions. These should not
            # have an ID passed in.anyway i'm at
            if child_id is not None:
                ent_dict['id'] = child_id
            ent_dict['parent_id'] = entity_id
            ent_dict['parent'] = collection
        if relations is not None:
            for rel_name, data in six.iteritems(relations):
                if isinstance(data, list):
                    ent_dict[rel_name] = []
                    for cls in data:
                        ent_dict[rel_name].append(self._return_class(cls))
                else:
                    ent_dict[rel_name] = self._return_class(data)
            ent_dict.pop('relations', None)
        return self.new(ent_type, properties=ent_dict)

    def _gen_classes(self, entities, child, child_id, entity_id, collection):
        """Iterate over entities, returning objects for each"""
        for entity in entities:
            e = self._return_class(entity, child, child_id, entity_id, collection)
            yield e

    @staticmethod
    def _construct_params(entity, include, full, page_limit,
                          page_offset, sort_by, parent, query):
        """Construct URL params"""
        if entity is not None:
            params = {}
        else:
            params = {'page_limit': page_limit,
                      'page_offset': page_offset,
                      'sort_by': sort_by,
                      'parent': parent,
                      'q': query, }

        # include can be either a string (e.g. 'advertiser'),
        # list of *non-traversable* relations (e.g. ['vendor', 'concept']),
        # or a list of lists/strings of traversable elements, e.g.
        # [['advertiser', 'agency'], 'vendor'],
        # [['advertiser', 'agency'], ['vendor', 'vendor_domains']]
        # If we're given a string, leave it as-is
        # If we're given a list, for each element:
        # -> If the item is a string, leave it as-is
        # -> If the item is a list, comma-join it
        # Examples from above:
        # include='advertiser' -> with=advertiser
        # include=['vendor', 'concept'] -> with=vendor&with=concept
        # include=[['advertiser', 'agency'], 'vendor']
        # -> with=advertiser,agency&with=vendor
        # include=[['advertiser', 'agency'], ['vendor', 'vendor_domains']]
        # -> with=advertiser,agency&with=vendor,vendor_domains
        if include is not None:
            if isinstance(include, list):
                for i, item in enumerate(include):
                    if isinstance(item, list):
                        include[i] = ','.join(item)
            params['with'] = include

        if isinstance(full, list):
            params['full'] = ','.join(full)
        elif full is True:
            params['full'] = '*'
        elif full is not None:
            params['full'] = full

        return params

    @staticmethod
    def _construct_url(collection, entity, child, limit):
        """Construct URL"""
        url = [collection, ]
        if entity is not None:
            url.append(str(entity))  # str so that we can use join

        child_id = None
        if child is not None:
            try:
                child_path = CHILD_PATHS[child.lower()]
            except AttributeError:
                raise ClientError("`child` must be a string of the entity to retrieve")
            except KeyError:
                raise ClientError("`child` must correspond to an entity in T1")
            # child_path should always be a tuple of (path, id). For children
            # that do not have IDs, like concepts and permissions, ID is 0
            if child_path[1]:
                child_id = child_path[1]
                url.append(child_path[0])
                # All values need to be strings for join
                url.append(str(child_path[1]))
            else:
                url.append(child_path[0])

        if isinstance(limit, dict):
            if len(limit) != 1:
                raise ClientError('Limit must consist of one parent collection '
                                  '(or chained parent collection) and a single '
                                  'value for it (e.g. {"advertiser": 1}, or '
                                  '{"advertiser.agency": 2)')
            url.extend(['limit',
                        '{0!s}={1:d}'.format(*next(six.iteritems(limit)))])

        return '/'.join(url), child_id

    def get(self,
            collection,
            entity=None,
            child=None,
            limit=None,
            include=None,
            full=None,
            page_limit=100,
            page_offset=0,
            sort_by='id',
            get_all=False,
            parent=None,
            query=None,
            count=False,
            _url=None,
            _params=None):
        """Main retrieval method for T1 Entities.

        :param collection: str T1 collection, e.g. "advertisers", "agencies"
        :param entity: int ID of entity being retrieved from T1
        :param child: str child, e.g. "dma", "acl"
        :param limit: dict[str]int query for relation entity, e.g. {"advertiser": 123456}
        :param include: str/list of relations to include, e.g. "advertiser",
            ["campaign", "advertiser"]
        :param full: str/bool when retrieving multiple entities, specifies which
            types to return the full record for.
            e.g. "campaign", True, ["campaign", "advertiser"]
        :param page_limit: int number of entities to return per query, 100 max
        :param page_offset: int offset for results returned.
        :param sort_by: str sort order. Default "id". e.g. "-id", "name"
        :param get_all: bool whether to retrieve all results for a query or just a single page
        :param parent: only return entities with this parent id
        :param query: str search parameter. Invoked by `find`
        :param count: bool return the number of entities as a second parameter
        :param _url: str shortcut to bypass URL determination.
        :param _params: dict query string parameters to bypass query determination
        :return: If:
            Collection is requested => generator over collection of entity objects
            Entity ID is provided => Entity object
            `count` is True => number of entities as second return val
        :raise ClientError: if page_limit > 100
        """
        if type(collection) == type and issubclass(collection, Entity):
            collection = MODEL_PATHS[collection]

        if page_limit > 100:
            raise ClientError('page_limit parameter must not exceed 100')

        child_id = None
        if _url is None:
            _url, child_id = self._construct_url(collection, entity, child, limit)

        if get_all:
            gen = self._get_all(collection,
                                entity=entity,
                                child=child,
                                include=include,
                                full=full,
                                sort_by=sort_by,
                                parent=parent,
                                query=query,
                                count=count,
                                _url=_url)
            if count:
                ent_count = next(gen)
                return gen, ent_count
            else:
                return gen

        if _params is None:
            _params = self._construct_params(entity, include, full, page_limit,
                                             page_offset, sort_by, parent, query)

        entities, ent_count = super(T1, self)._get(PATHS['mgmt'], _url, params=_params)

        if ent_count == 1:
            return self._return_class(next(entities), child, child_id, entity, collection)

        ent_gen = self._gen_classes(entities, child, child_id, entity, collection)
        if count:
            return ent_gen, ent_count
        else:
            return ent_gen

    def get_all(self, collection, **kwargs):
        """Retrieves all entities in a collection. Has same signature as .get."""
        kwargs.pop('get_all', None)
        return self.get(collection, get_all=True, **kwargs)

    def _get_all(self, collection, **kwargs):
        """Construct iterator to get all entities in a collection.

        Pages over 100 entities.
        This method should not be called directly: it's called from T1.get.
        """
        _, num_recs = super(T1, self)._get(PATHS['mgmt'], kwargs['_url'], params={
            'page_limit': 1,
            'parent': kwargs.get('parent'),
            'q': kwargs.get('query')
        })

        if kwargs.get('count'):
            yield num_recs

        for page_offset in six.moves.range(0, num_recs, 100):
            # get_all=False, otherwise we could go in a loop
            gen = self.get(collection,
                           _url=kwargs['_url'],
                           entity=kwargs.get('entity'),
                           include=kwargs.get('include'),
                           full=kwargs.get('full'),
                           page_offset=page_offset,
                           sort_by=kwargs.get('sort_by'),
                           parent=kwargs.get('parent'),
                           query=kwargs.get('query'),
                           get_all=False)
            if not isinstance(gen, GeneratorType):
                gen = iter([gen])
            for item in gen:
                yield item

    # def get_sub(self, collection, entity, sub, *args):
    #   pass

    @staticmethod
    def _parse_candidate(candidate):
        """Parse filter candidates so that you can use None, True, False."""
        val = candidate
        if candidate is None:
            val = "null"
        elif candidate is True:
            val = "1"
        elif candidate is False:
            val = "0"
        return val

    def find(self, collection, variable, operator, candidates, **kwargs):
        """Find objects based on query criteria. Helper method for T1.get,
        with same return values.

        :param collection: str T1 collection, e.g. "advertisers", "agencies"
        :param variable: str Field to query for, e.g. "name". If operator is
            terminalone.filters.IN, this is ignored and None can be provided
        :param operator: str Arithmetic operator, e.g. "=:". Package provides
            helper object filters to help, e.g. terminalone.filters.IN or
            terminalone.filters.CASE_INS_STRING
        :param candidates: str/int/list values to search for. list only if
            operator is IN.
        :param kwargs: additional keyword args to pass on to T1.get. See that
            method's signature for details.
        :return: generator over collection of objects matching query
        :raise TypeError: if operator is IN and candidates not provided as list
        """
        if operator == filters.IN:
            if not isinstance(candidates, list):
                raise TypeError('`candidates` must be list of entities for `IN`')
            query = '(' + ','.join(str(c) for c in candidates) + ')'
        else:
            query = operator.join([variable, self._parse_candidate(candidates)])
        return self.get(collection, query=query, **kwargs)


T1Service = T1
