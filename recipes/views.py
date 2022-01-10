from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from recipes.models import Recipe

User = get_user_model()

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


class RecipesByAuthor(ListView):
    model = Recipe
    template_name = 'recipes_by_author.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        author = get_object_or_404(User, pk=self.kwargs['pk'])
        return Recipe.objects.filter(author=author).\
            select_related('author').\
            prefetch_related('tags')


class RecipeCreateView(CreateView):
    model = Recipe
    template_name = 'recipe_create.html'
    fields = ['title',
              'tags',
              'ingridients',
              'time_cooking',
              'description',
              'image',
              ]





