from django.shortcuts import render
from django.views.generic import ListView, DetailView

from recipes.models import Recipe


# def index(request):
#     recipes = Recipe.objects.all().select_related('author').prefetch_related('tags')
#     print(recipes.query)
#     return render(request, 'index.html', {'recipes': recipes})


class RecipesListView(ListView):
    model = Recipe
    template_name = 'index.html'
    context_object_name = 'recipes'
    queryset = Recipe.objects.all(). \
        select_related('author'). \
        prefetch_related('tags')


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'
    queryset = Recipe.objects.filter(pk=1).select_related('author').prefetch_related('tags')


