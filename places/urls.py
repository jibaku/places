from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('places.views',
    url(r'^(?P<place_slug>[-\w]+)/$', 'place_detail', name='places-detail'),
)
