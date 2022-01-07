from django.contrib import admin
from recipes.models import Recipe, Follow, Ingridient, RecipeIngredient, Tags


admin.site.register(Recipe)
admin.site.register(Ingridient)
admin.site.register(Follow)
admin.site.register(RecipeIngredient)
admin.site.register(Tags)

