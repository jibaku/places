# -*- coding: utf-8 -*-

from django.contrib import admin
from places.models import Place

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'longitude', 'latitude')
    list_filter = ('site',)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name','description',)

admin.site.register(Place, PlaceAdmin)