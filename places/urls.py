from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import (PlaceAddView, PlaceDetailView, PlaceListView,
                    UserPlaceListView)

urlpatterns = [
    url(r'^$', PlaceListView.as_view(), name='places-index'),
    url(r'^show/(?P<category_slug>[-\w]+)/$', PlaceListView.as_view(), name='places-index'),
    url(r'^add/$', login_required(PlaceAddView.as_view()), name='places-new'),
    url(r'^by/(?P<username>[-\w]+)/$', UserPlaceListView.as_view(), name='places-user-list'),
    url(r'^(?P<slug>[-\w]+)/$', PlaceDetailView.as_view(), name='places-detail'),
]