# -*- coding: utf-8 -*-
"""Places app forms."""
from django import forms
from django.template.defaultfilters import slugify

from places.models import Place


class AddPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'position', 'city', 'is_public', 'description', 'site')
        widgets = {
            'site': forms.HiddenInput(),
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
