from django import forms
from django.forms import ModelForm

from recipes.models import Recipe, Tags


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title',
                  'tags',
                  'ingridients',
                  'time_cooking',
                  'description',
                  'image',
                  ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, data=None, *args, **kwargs):

        super().__init__(data)
        if data:
            for i in data:
                print(i)
