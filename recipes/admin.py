from django.contrib import admin
from recipes.models import Recipe, Follow, Ingridient, RecipeIngredient


admin.site.register(Recipe)
admin.site.register(Ingridient)
admin.site.register(Follow)
admin.site.register(RecipeIngredient)

