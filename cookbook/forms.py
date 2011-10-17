from django import forms
from django.forms import Textarea
from cookbook.models import *

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        widgets = {
            'directions': Textarea(attrs={'class': 'tinymce'}),
            'ingredients': Textarea(attrs={'class': 'tinymce'}),
            'healthier_substitutions': Textarea(attrs={'class': 'tinymce'}),
            'tips': Textarea(attrs={'class': 'tinymce'}),
        }

    
