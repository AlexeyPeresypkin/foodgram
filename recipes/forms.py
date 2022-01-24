from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from recipes.models import Recipe, Tags, Ingridient


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
        if data:
            data = data.copy()
            for k, v in data.items():
                print(k, v)
            for tag in ('breakfast', 'lunch', 'dinner'):
                if tag in data:
                    data.update({'tags': Tags.objects.get(slug=tag)})
            ingridients = self.get_ingridients(data)
            print(ingridients)
            for ingridient in ingridients:
                try:
                    data.update(
                        {'ingridients': Ingridient.objects.get(
                            title=ingridient)}
                    )
                except Ingridient.DoesNotExist:
                    ValidationError(
                        'Нет такого ингридиента, выберите из списка'
                    )
            self.quantity = self.get_quantity(data)
        super().__init__(data=data, *args, **kwargs)

    def get_ingridients(self, data):
        ingridients = []
        for key in data:
            if key.startswith('nameIngredient'):
                ingridients.append(data[key])
        return ingridients

    def get_quantity(self, data):
        result = {}
        for key in data:
            if key.startswith('nameIngredient'):
                n = key.split('_')[1]
                result[data[f'nameIngredient_{n}']] = data[
                    f'valueIngredient_{n}']
        return result
