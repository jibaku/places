from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from django.template.defaultfilters import slugify

from .models import Place
from .forms import AddPlaceForm


class PlaceListView(ListView):
    def get_queryset(self):
        return Place.objects.public()


class UserPlaceListView(ListView):
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
        context['center'] = self.get_queryset().collect().centroid
        return context


class PlaceDetailView(DetailView):
    slug_field = 'slug'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            queryset = Place.objects.for_user(self.request.user)
        else:
            queryset = Place.objects.public()
        return queryset


class PlaceAddView(CreateView):
    template_name = 'places/place_form.html'

    def get_form_class(self):
        return AddPlaceForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(form.instance.name)
        return super(PlaceAddView, self).form_valid(form)
