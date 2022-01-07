from django.shortcuts import render
from recipes.models import Recipe


def index(request):
    recipe_list = Recipe.objects.all()
    return render(request, 'index.html')
