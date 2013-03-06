# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.gis.db import models as gis_models

from places.models import Place
from places.widgets import GoogleMapPointWidget


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'is_public', 'city', 'added_on', 'updated_on')
    list_filter = ('site', 'is_public')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name', 'description',)
    formfield_overrides = {
        gis_models.PointField: {'widget': GoogleMapPointWidget},
    }
    actions = ['mark_as_public', 'mark_as_private']

    def mark_as_public(self, request, queryset):
        queryset.update(is_public=True)
    mark_as_public.short_description = u"Mark as public"

    def mark_as_private(self, request, queryset):
        queryset.update(is_public=False)
    mark_as_private.short_description = u"Mark as private"

admin.site.register(Place, PlaceAdmin)
