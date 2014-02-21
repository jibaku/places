from django import forms
from django.template.defaultfilters import slugify

from .models import Place
from .widgets import GoogleMapPointWidget


class AddPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'position', 'city', 'is_public', 'description', 'site')
        widgets = {
            'site': forms.HiddenInput(),
            'position': GoogleMapPointWidget(attrs={'allow_bigger': False, 'min_width': 850, 'min_height': 250}),
        }

    def clean(self):
        if 'name' in self.cleaned_data:
            slug = slugify(self.cleaned_data['name'])
            try:
                Place.objects.get(site=self.cleaned_data['site'], slug=slug)
                raise forms.ValidationError("slug already exist.")
            except Place.DoesNotExist:
                pass
        return self.cleaned_data
