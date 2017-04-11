# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.sites.models import Site
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from places.managers import PlaceManager


@python_2_unicode_compatible
class Category(models.Model):
    # site = models.ForeignKey(Site, default=settings.SITE_ID)
    name = models.CharField(_("Name"), max_length=200)
    slug = models.SlugField(_("Slug"))
    # private_icon
    # public_icon

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('places-category', [self.slug])


@python_2_unicode_compatible
class Place(models.Model):
    site = models.ForeignKey(Site, default=settings.SITE_ID)
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    name = models.CharField(_("Name"), max_length=200)
    slug = models.SlugField(_("Slug"))

    longitude = models.FloatField(_("Longitude"), blank=True, editable=False)
    latitude = models.FloatField(_("Latitude"), blank=True, editable=False)
    position = models.PointField(_("Position"), srid=4326, blank=True, null=True)
    is_public = models.BooleanField(_("Is public?"), db_index=True, default=False)

    street = models.CharField(_("Street"), blank=True, max_length=250)
    postal_code = models.CharField(_("Postal code"), blank=True, max_length=25)
    city = models.CharField(_("City"), blank=True, max_length=100)

    description = models.TextField(_("Description"), blank=True)
    main_picture = models.ImageField(upload_to='places/main_picture/', blank=True, null=True)

    added_on = models.DateTimeField(default=datetime.datetime.now, editable=False)
    updated_on = models.DateTimeField(editable=False)

    objects = PlaceManager()

    # place / people / club / boutique

    class Meta:
        unique_together = (
            ('site', 'slug')
        )
        verbose_name = _('place')
        verbose_name_plural = _('places')

    @models.permalink
    def get_absolute_url(self):
        return ('places-detail', [self.slug])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Updating latitude/longitude when position is updated."""
        if self.position:
            self.latitude = self.position.x
            self.longitude = self.position.y
        self.updated_on = datetime.datetime.now()
        super(Place, self).save(*args, **kwargs)


class PlaceLink(models.Model):
    WEBSITE = 'website'
    FACEBOOK = 'facebook'
    TWITTER = 'twitter'
    INSTAGRAM = 'instagram'

    LINK_TYPES = (
        (WEBSITE, 'Website'),
        (FACEBOOK, 'Facebook'),
        (TWITTER, 'Twitter'),
        (INSTAGRAM, 'Instagram'),
    )
    place = models.ForeignKey(Place)
    url = models.URLField()
    link_type = models.CharField(choices=LINK_TYPES, default=WEBSITE, max_length=20)
