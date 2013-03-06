from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from django.conf import settings
from django.template.defaultfilters import slugify

from .models import Place
from .forms import AddPlaceForm


class PlaceListView(ListView):
    def get_queryset(self):
        queryset = Place.objects.filter(site__id=settings.SITE_ID)
        queryset = queryset.filter(is_public=True)
        return queryset


class PlaceDetailView(DetailView):
    slug_field = 'slug'

    def get_queryset(self):
        queryset = Place.objects.filter(site__id=settings.SITE_ID)
        if self.request.user.is_authenticated():
            filters = Q(is_public=True) | Q(is_public=False, user=self.request.user)
        else:
            filters = Q(is_public=True)
        queryset = queryset.filter(filters)
        return queryset


class UserPlaceListView(ListView):
    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        show_all = False
        if user == self.request.user:
            show_all = True

        queryset = Place.objects.filter(site__id=settings.SITE_ID).filter(user=user)
        if not show_all:
            queryset = queryset.filter(is_public=True)
        print queryset.query
        return queryset


class PlaceAddView(CreateView):
    template_name = 'places/place_form.html'

    def get_form_class(self):
        return AddPlaceForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(form.instance.name)
        return super(PlaceAddView, self).form_valid(form)
