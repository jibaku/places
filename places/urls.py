from django.conf.urls.defaults import *

urlpatterns = patterns('places.views',
    url(r'^$', 'place_list', name='places-index'),
    url(r'^(?P<place_slug>[-\w]+)/$', 'place_detail', name='places-detail'),
)
