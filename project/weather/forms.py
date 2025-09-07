from django.forms import ModelForm, TextInput
from .models import City
from django import forms

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'}),
        } #updates the input class to have the correct Bulma class and placeholder
        
    def clean_name(self):
        name = self.cleaned_data['name'].strip()  # remove spaces
        if not name:
            raise forms.ValidationError("City name cannot be empty.")
        return name