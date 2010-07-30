from django.views.generic.list_detail import object_detail
from places.models import Place
from django.conf import settings

def place_detail(request, place_slug):
    queryset = Place.objects.filter(site__id=settings.SITE_ID)
    return object_detail(request, queryset=queryset, slug=place_slug, slug_field='slug')