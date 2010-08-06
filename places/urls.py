from django.conf.urls.defaults import *

urlpatterns = patterns('places.views',
    url(r'^(?P<place_slug>[-\w]+)/$', 'place_detail', name='places-detail'),
)
