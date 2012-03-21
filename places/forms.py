from django import forms
from django.template.defaultfilters import slugify

from places.models import Place
from places.widgets import GoogleMapPointWidget

class AddPlaceForm(forms.ModelForm):
	class Meta:
		model = Place
		fields = ('name','position', 'is_public', 'description', 'site')
		widgets = {
            'site': forms.HiddenInput(),
            'position': GoogleMapPointWidget(attrs={'allow_bigger':False}),
        }
	
	def clean(self):
		if self.cleaned_data.has_key('name'):
			slug = slugify(self.cleaned_data['name'])
			try:
				Place.objects.get(site=self.cleaned_data['site'], slug=slug)
				raise forms.ValidationError("slug already exist.")
			except Place.DoesNotExist:
				pass
		return self.cleaned_data
