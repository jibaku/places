from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from django.template.defaultfilters import slugify

from .models import Place, Category
from .forms import AddPlaceForm


class PlaceListView(ListView):
    """
    List all the public places
    """
    def get_queryset(self):
        qs = Place.objects.public()
        if 'category_slug' in self.kwargs:
            qs = qs.filter(category=get_object_or_404(Category, slug=self.kwargs['category_slug']))
        return qs


class UserPlaceListView(ListView):
    """
    List the places for a given user.
    """
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

    def get_context_data(self, **kwargs):
        context = super(PlaceDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            nearby = Place.objects.for_user(self.request.user).distance(self.object.position).exclude(id=self.object.id)[:5]
        else:
            nearby = Place.objects.public().distance(self.object.position).exclude(id=self.object.id)[:5]
        context['nearby'] = nearby
        return context
        

class PlaceAddView(CreateView):
    template_name = 'places/place_form.html'

    def get_form_class(self):
        return AddPlaceForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(form.instance.name)
        return super(PlaceAddView, self).form_valid(form)
