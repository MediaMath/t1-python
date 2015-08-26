# -*- coding: utf-8 -*-
"""Utility for generating PMP-D tags"""

from ..models import Publisher, PublisherSite, PlacementSlot

TYPE_MAP = {
    'iframe': 1,
    'js': 2,
    'script': 2,
    'js/iframe': 3,
    'script/iframe': 3,
}

IFRAME_TAG = ('<iframe width={width} height={height} scrolling=no frameborder=0'
              ' marginwidth=0 marginheight=0 src="http://tags.mathtag.com'
              '/ad/iframe/{pub_id}/{site_id}?pmp={slot_id}&click=&rfr='
              '{{INSERT_PUBLISHER_URL}}&random={{INSERT_CACHEBUSTER}}"></iframe>')

SCRIPT_TAG = ('<script type="text/javascript" src="http://tags.mathtag.com'
              '/ad/js/{pub_id}/{site_id}?pmp={slot_id}&click=&rfr='
              '{{INSERT_PUBLISHER_URL}}&random={{INSERT_CACHEBUSTER}}"></script>')


def generate_pmpd_tag(tag_type, placement_slot, publisher_site, publisher):
    """Generate PMP-D tag from already-created values.

    :param tag_type: enum{'iframe', 'js', 'js/iframe'} type of tag
    :param placement_slot: PlacementSlot instance
    :param publisher_site: PublisherSite instance
    :param publisher: Publisher instance
    :return: str tag
    :raise: TypeError if param is wrong type.
        ValueError if invalid tag_type.
    """
    if not isinstance(placement_slot, PlacementSlot):
        raise TypeError('placement_slot should be a PlacementSlot instance')
    if not isinstance(publisher_site, PublisherSite):
        raise TypeError('publisher_site should be a PublisherSite instance')
    if not isinstance(publisher, Publisher):
        raise TypeError('publisher should be a Publisher instance')
    try:
        typ = TYPE_MAP[tag_type]
    except KeyError:
        raise ValueError('Invalid tag_type')

    if typ == 1:
        tag = IFRAME_TAG
    elif typ == 2:
        tag = SCRIPT_TAG
    else:
        tag = SCRIPT_TAG + '<noscript>' + IFRAME_TAG + '</noscript>'

    return tag.format(pub_id=publisher.id,
                      site_id=publisher_site.id,
                      slot_id=placement_slot.id,
                      width=placement_slot.width,
                      height=placement_slot.height)
