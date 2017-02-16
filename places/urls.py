# -*- coding: utf-8 -*-
"""Definition of places app urls."""
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from places.views import (PlaceAddView, PlaceDetailView, PlaceListView,
                          UserPlaceListView)

urlpatterns = [
    url(r'^$', PlaceListView.as_view(), name='places-index'),
    url(r'^add/$', login_required(PlaceAddView.as_view()), name='places-new'),
    url(r'^filter/(?P<category_slug>[-\w]+)/$', PlaceListView.as_view(), name='places-category'),
    url(r'^by/(?P<username>[-\w]+)/$', UserPlaceListView.as_view(), name='places-user-list'),
    url(r'^(?P<slug>[-\w]+)/$', PlaceDetailView.as_view(), name='places-detail'),
]
