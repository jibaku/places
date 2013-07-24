# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

from places.models import Place

register = template.Library()


class PlacesNode(template.Node):
    def __init__(self, var_name, filters):
        self.var_name = var_name
        self.filters = filters

    def render(self, context):
        context[self.var_name] = Place.objects.filter(site__id=settings.SITE_ID).order_by('name')
        return ''


@register.tag(name="places_filter")
def places_filter(parser, token):
    """
    {% places_filter <filters> as places %}
    """
    tokens = token.split_contents()
    raise_error = False
    if len(tokens) == 4:
        if tokens[0] == 'places_filter' and tokens[2] == 'as':
            var_name = tokens[3]
            filters = tokens[1]
        else:
            raise_error = True
    elif len(tokens) == 3:
        if tokens[0] == 'places_filter' and tokens[1] == 'as':
            var_name = tokens[2]
            filters = None
        else:
            raise_error = True

    if raise_error:
        raise template.TemplateSyntaxError, "%r tag must be used with %s" % (tokens[0], "{% categories as categories %}")
    else:
        return PlacesNode(var_name, filters)


@register.inclusion_tag('places/inclusion_tag/staticmap.html')
def staticmap(latitude, longitude, html_size="200x500"):
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
    }


@register.simple_tag
def user_places_count(user):
    return Place.objects.filter(user=user).count()
