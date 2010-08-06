# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings

class Place(models.Model):
    site = models.ForeignKey(Site, default=settings.SITE_ID)
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    longitude = models.FloatField(blank=True)
    latitude = models.FloatField(blank=True)
    
    street = models.CharField(blank=True, max_length=250)
    postal_code = models.CharField(blank=True, max_length=25)
    city = models.CharField(blank=True, max_length=100)
    
    description = models.TextField(blank=True)

    class Meta:
        unique_together = (
            ('site', 'slug')
        )
    
    def __unicode__(self):
        return self.name
