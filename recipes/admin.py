from django.contrib import admin
from recipes.models import Recipe, Follow, Ingridient, RecipeIngredient, Tags, \
    Favorite, ShopList


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', ]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingridient)
admin.site.register(Follow)
admin.site.register(RecipeIngredient)
admin.site.register(Tags)
admin.site.register(Favorite)
admin.site.register(ShopList)
