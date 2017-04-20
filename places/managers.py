# -*- coding: utf-8 -*-
"""Managers for the app models."""

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.gis.db import models
from django.db.models import Q
from django.contrib.gis.db.models.query import GeoQuerySet


class PlaceQuerySet(GeoQuerySet):
    def published(self):
        return self.filter(status=self.model.PUBLISHED)

    def draft(self):
        return self.filter(status=self.model.DRAFT)

    def deleted(self):
        return self.filter(status=self.model.DELETED)

    def public(self):
        return self.filter(is_public=True)

    def for_user(self, user):
        filters = Q(is_public=True) | Q(is_public=False, user=user)
        return self.filter(filters)


class PlaceManager(models.GeoManager):
    def get_queryset(self):
        return PlaceQuerySet(self.model, using=self._db)

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
        return self.for_site(site_id).public()

    def for_user(self, user, site_id=None):
        return self.for_site(site_id).for_user(user)

    def user_public_places(self, user, site_id=None):
        return self.for_site(site_id).public().for_user(user=user)
