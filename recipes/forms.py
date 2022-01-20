from django import forms
from django.forms import ModelForm

from recipes.models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title',
                  'tags',
                  # 'ingridients',
                  'time_cooking',
                  'description',
                  'image',
                  ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
