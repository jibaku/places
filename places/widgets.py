from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.contrib.gis.geos import Point

DEFAULT_POINT = Point(7,47)
MINIMIZED_MAPS_HEIGHT = 300
MINIMIZED_MAPS_WIDTH = 400
MAXIMIZED_MAPS_HEIGHT = 600
MAXIMIZED_MAPS_WIDTH = 800

class GoogleMapPointWidget(forms.widgets.Widget):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js',
            'http://maps.googleapis.com/maps/api/js?sensor=false'
        )
    def __init__(self, *args, **kw):
        super(GoogleMapPointWidget, self).__init__(*args, **kw)
        self.hidden_input = forms.widgets.HiddenInput()
        
    def render(self, name, value, *args, **kwargs):
        if value is None:
            value = DEFAULT_POINT
            zoom_level = 8
        else:
            zoom_level = 12
        
        context = {
            'zoom_level':zoom_level,
            'point':value,
            'name':name,
            'min_width':MINIMIZED_MAPS_WIDTH,
            'min_height':MINIMIZED_MAPS_HEIGHT,
            'max_width':MAXIMIZED_MAPS_WIDTH,
            'max_height':MAXIMIZED_MAPS_HEIGHT,
        }
        
        javascript = render_to_string('places/javascript/point_gmap.js', context)
        
        html = self.hidden_input.render("%s" % name, None, dict(id='id_%s' % name))
        html += "<button id='min_%s'>-</button>" % name
        html += "<button id='max_%s'>+</button><br/>" % name
        map_options = {
            'name':name,
            'min_width':MINIMIZED_MAPS_WIDTH,
            'min_height':MINIMIZED_MAPS_HEIGHT,
        }
        html += "<div id=\"map_%(name)s\" style=\"width: %(min_width)spx; height: %(min_height)spx\"></div>" % map_options
        return mark_safe(javascript+html)
