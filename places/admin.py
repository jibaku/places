# -*- coding: utf-8 -*-
"""Places admin."""
from __future__ import unicode_literals

from django.contrib.gis import admin
from django.utils.translation import ugettext_lazy as _

from places.models import Category, Place, PlaceLink


class PlaceLinkInline(admin.TabularInline):
    model = PlaceLink


class PlaceAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'category', 'user', 'city',
                    'added_on', 'updated_on', 'status', 'is_public')
    list_filter = ('site', 'category', 'is_public', 'added_on', 'status')
    date_hierarchy = ('added_on')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name', 'description',)
    actions = [
        'mark_as_public', 'mark_as_private',
        'mark_as_draft', 'mark_as_published', 'mark_as_deleted'
    ]
    inlines = [PlaceLinkInline]

    def mark_as_public(self, request, queryset):
        queryset.update(is_public=True)
    mark_as_public.short_description = _("Mark as public")

    def mark_as_private(self, request, queryset):
        queryset.update(is_public=False)
    mark_as_private.short_description = _("Mark as private")

    def mark_as_draft(self, request, queryset):
        queryset.update(status=Place.DRAFT)
    mark_as_draft.short_description = _("Mark as draft")

    def mark_as_published(self, request, queryset):
        queryset.update(status=Place.PUBLISHED)
    mark_as_published.short_description = _("Mark as published")

    def mark_as_deleted(self, request, queryset):
        queryset.update(status=Place.DELETED)
    mark_as_deleted.short_description = _("Mark as deleted")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Place, PlaceAdmin)
admin.site.register(Category, CategoryAdmin)


@admin.register(PlaceLink)
class PlaceLinkAdmin(admin.ModelAdmin):
    list_display = ('place', 'url', 'link_type')
    list_filter = ('link_type',)
