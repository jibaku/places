from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('places.views',
    url(r'^$', 'place_list', name='places-index'),
    url(r'^add/$', 'place_add', name='places-new'),
    url(r'^by/(?P<username>[-\w]+)/$', 'user_place_list', name='places-user-list'),
    url(r'^(?P<place_slug>[-\w]+)/$', 'place_detail', name='places-detail'),
)
