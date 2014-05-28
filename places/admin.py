# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.gis.db import models as gis_models
from django.utils.translation import ugettext_lazy as _

from places.models import Place, Category
from places.widgets import GoogleMapPointWidget


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'is_public','category', 'user', 'city', 'added_on', 'updated_on')
    list_filter = ('site', 'category', 'is_public', 'added_on')
    date_hierarchy = ('added_on')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name', 'description',)
    formfield_overrides = {
        gis_models.PointField: {'widget': GoogleMapPointWidget},
    }
    actions = ['mark_as_public', 'mark_as_private']

    def mark_as_public(self, request, queryset):
        queryset.update(is_public=True)
    mark_as_public.short_description = _(u"Mark as public")

    def mark_as_private(self, request, queryset):
        queryset.update(is_public=False)
    mark_as_private.short_description = _(u"Mark as private")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Place, PlaceAdmin)
admin.site.register(Category, CategoryAdmin)
