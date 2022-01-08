from django.shortcuts import render
from recipes.models import Recipe


def index(request):
    recipes = Recipe.objects.all().select_related('author').prefetch_related('tags')
    return render(request, 'index.html', {'recipes': recipes})


