# -*- coding: utf-8 -*-
"""Views for places app."""
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db.models import Collect
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from places.forms import AddPlaceForm
from places.models import Category, Place


class PlaceListView(ListView):
    """List all the public places."""

    category_slug = None

    def get_category_slug(self):
        if self.category_slug is not None:
            return self.category_slug
        else:
            return self.kwargs.get('category_slug')

    @property
    def category(self):
        print(self.get_category_slug())
        if self.get_category_slug() is not None:
            return get_object_or_404(Category, slug=self.get_category_slug())
        return None

    def get_queryset(self):
        qs = Place.objects.public().published()
        category = self.category
        if category is not None:
            qs = qs.filter(category=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super(PlaceListView, self).get_context_data(**kwargs)
        context['current_category'] = self.category
        return context


class UserPlaceListView(ListView):
    """List the places for a given user."""

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        if user == self.request.user:
            queryset = Place.objects.for_user(user=user)
        else:
            queryset = Place.objects.user_public_places(user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserPlaceListView, self).get_context_data(**kwargs)
        context['center'] = self.get_queryset().aggregate(position_center=Collect('position'))['position_center'].centroid
        return context


class PlaceDetailView(DetailView):
    slug_field = 'slug'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            queryset = Place.objects.for_user(self.request.user)
        else:
            queryset = Place.objects.public()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PlaceDetailView, self).get_context_data(**kwargs)
        nearby_items = getattr(settings, 'PLACES_RELATED_COUNT', 5)
        try:
            # TODO: put as place method
            if self.request.user.is_authenticated():
                nearby = Place.objects.for_user(self.request.user).distance(self.object.position).exclude(id=self.object.id)
            else:
                nearby = Place.objects.public().distance(self.object.position).exclude(id=self.object.id)
            nearby = nearby.order_by('distance')
            nearby = nearby[:nearby_items]
        except ValueError:
            nearby = Place.objects.public().order_by('?')[:nearby_items]
        context['nearby'] = nearby
        from django.core.serializers import serialize
        json = serialize('geojson',
                         Place.objects.filter(id__in=[self.object.id]),
                         geometry_field='position',
                         fields=('name',),
                         indent=4)
        context['geojson'] = json
        return context


class PlaceAddView(CreateView):
    template_name = 'places/place_form.html'

    def get_form_class(self):
        return AddPlaceForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(form.instance.name)
        return super(PlaceAddView, self).form_valid(form)
