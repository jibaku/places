from django.conf.urls import patterns, url
from .views import PlaceListView, PlaceDetailView, UserPlaceListView, PlaceAddView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', PlaceListView.as_view(), name='places-index'),
    url(r'^add/$', login_required(PlaceAddView.as_view()), name='places-new'),
    url(r'^by/(?P<username>[-\w]+)/$', UserPlaceListView.as_view(), name='places-user-list'),
    url(r'^(?P<slug>[-\w]+)/$', PlaceDetailView.as_view(), name='places-detail'),
)
