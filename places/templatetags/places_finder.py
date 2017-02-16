# -*- coding: utf-8 -*-
"""Places app places_finder template tags."""
from __future__ import unicode_literals

from django import template

from places.models import Place

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

    return {
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
