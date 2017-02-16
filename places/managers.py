# -*- coding: utf-8 -*-
"""Managers for the app models."""

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.gis.db import models
from django.db.models import Q


class PlaceManager(models.GeoManager):
    def for_site(self, site_id=None):
        if site_id is None:
            site_id = settings.SITE_ID
        return self.filter(site__id=site_id)

    def public(self, site_id=None):
        """
        Return the public places.

        By default for the current website, or for the site whose ID is passed
        as *site_id* parameter.
        """
        queryset = self.for_site(site_id)
        queryset = queryset.filter(is_public=True)
        return queryset

    def for_user(self, user, site_id=None):
        filters = Q(is_public=True) | Q(is_public=False, user=user)
        queryset = self.for_site(site_id)
        queryset = queryset.filter(filters)
        return queryset

    def user_public_places(self, user, site_id=None):
        return self.for_site(site_id).filter(is_public=True, user=user)
