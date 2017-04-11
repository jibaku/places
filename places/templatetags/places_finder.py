# -*- coding: utf-8 -*-
"""Places app places_finder template tags."""
from __future__ import unicode_literals

from django import template
from django.conf import settings

from places.models import Place
from places.utils import sign_googleapi_url

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

register = template.Library()


@register.inclusion_tag('places/inclusion_tag/staticmap.html')
def staticmap(latitude, longitude, html_size="200x500", alt=None):
    """Return a static map."""
    try:
        height, width = html_size.split("x")
        height, width = int(height), int(width)
    except ValueError:
        err = 'staticmap third attribute must be in the form WIDTHxHEIGHT'
        err += '(like "300x400")'
        raise template.TemplateSyntaxError(err)
    key = getattr(settings, 'GOOGLE_API_KEY', None)
    secret = getattr(settings, 'GOOGLE_API_SECRET', None)
    params = {
        'center': '{latitude:f},{longitude:f}'.format(latitude=latitude, longitude=longitude),
        'zoom': "17",
        'maptype': "hybrid",
        'size': '{width}x{height}'.format(width=width, height=height),
        'sensor': 'false',
        # 'markers':'size:big|color:blue|{latitude:f},{longitude:f}'.format(latitude=latitude, longitude=longitude),
    }
    if key is not None:
        params['key'] = key
    url = "{path}?{query}".format(path="https://maps.googleapis.com/maps/api/staticmap",
                                  query=urlencode(params))
    if secret is not None:
        url = sign_googleapi_url(url, secret)

    return {
        'url': url,
        'lat': latitude,
        'long': longitude,
        'height': height,
        'width': width,
        'alt': alt,
    }


@register.simple_tag
def user_places_count(user):
    """Count the number of places for a given user."""
    return Place.objects.filter(user=user).count()
