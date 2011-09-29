# -*- coding: utf-8 -*-
import datetime

from django.contrib.gis.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings

class Place(models.Model):
    site = models.ForeignKey(Site, default=settings.SITE_ID)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    longitude = models.FloatField(blank=True, editable=False)
    latitude = models.FloatField(blank=True, editable=False)
    position = models.PointField(srid=4326, blank=True, null=True)
    is_public = models.BooleanField(db_index=True)

    street = models.CharField(blank=True, max_length=250)
    postal_code = models.CharField(blank=True, max_length=25)
    city = models.CharField(blank=True, max_length=100)
    
    description = models.TextField(blank=True)

    #added_on = models.DateTimeField(default=datetime.datetime.now, editable=False)
    #updated_on = models.DateTimeField(editable=False)

    class Meta:
        unique_together = (
            ('site', 'slug')
        )
    
    @models.permalink
    def get_absolute_url(self):
        return ('places-detail', [self.slug])
    
    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Updating latitude/longitude when position is updated
        """
        self.latitude = self.position.x
        self.longitude = self.position.y
        super(Place, self).save(*args, **kwargs)