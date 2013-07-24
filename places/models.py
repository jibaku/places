# -*- coding: utf-8 -*-
import datetime

from django.contrib.gis.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .managers import PlaceManager


class Place(models.Model):
    site = models.ForeignKey(Site, default=settings.SITE_ID)
    user = models.ForeignKey(User)
    name = models.CharField(_("Name"), max_length=200)
    slug = models.SlugField(_("Slug"))

    longitude = models.FloatField(_("Longitude"), blank=True, editable=False)
    latitude = models.FloatField(_("Latitude"), blank=True, editable=False)
    position = models.PointField(_("Position"), srid=4326, blank=True, null=True)
    is_public = models.BooleanField(_("Is public?"), db_index=True)

    street = models.CharField(_("Street"), blank=True, max_length=250)
    postal_code = models.CharField(_("Postal code"), blank=True, max_length=25)
    city = models.CharField(_("City"), blank=True, max_length=100)

    description = models.TextField(_("Description"), blank=True)

    added_on = models.DateTimeField(default=datetime.datetime.now, editable=False)
    updated_on = models.DateTimeField(editable=False)

    objects = PlaceManager()

    class Meta:
        unique_together = (
            ('site', 'slug')
        )
        verbose_name = _('Place')
        verbose_name_plural = _('Places')

    @models.permalink
    def get_absolute_url(self):
        return ('places-detail', [self.slug])

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Updating latitude/longitude when position is updated
        """
        if self.position:
            self.latitude = self.position.x
            self.longitude = self.position.y
        self.updated_on = datetime.datetime.now()
        super(Place, self).save(*args, **kwargs)
