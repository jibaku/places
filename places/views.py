from django.views.generic.list_detail import object_detail, object_list
from places.models import Place
from django.conf import settings

def place_list(request):
    queryset = Place.objects.filter(site__id=settings.SITE_ID)
    return object_list(request, queryset=queryset)

def place_detail(request, place_slug):
    queryset = Place.objects.filter(site__id=settings.SITE_ID)
    return object_detail(request, queryset=queryset, slug=place_slug, slug_field='slug')