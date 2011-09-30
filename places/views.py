from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.shortcuts import redirect
from django.template.defaultfilters import slugify

from places.models import Place
from places.forms import AddPlaceForm

def place_list(request):
    queryset = Place.objects.filter(site__id=settings.SITE_ID).filter(is_public=True)
    return object_list(request, queryset=queryset)

@login_required
def user_place_list(request, username=None):
	if username is not None:
		user = get_object_or_404(User, username=username)
	else:
		user = request.user
	queryset = Place.objects.filter(site__id=settings.SITE_ID).filter(user=user)
	return object_list(request, queryset=queryset)	

def place_detail(request, place_slug):
    queryset = Place.objects.filter(site__id=settings.SITE_ID)
    return object_detail(request, queryset=queryset, slug=place_slug, slug_field='slug')

@login_required
def place_add(request):
	if request.POST:
		form = AddPlaceForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.slug = slugify(instance.name)
			instance.save()
			return redirect(instance.get_absolute_url())
	else:
		form = AddPlaceForm()
	return direct_to_template(request, template='places/place_form.html', extra_context={'form':form})