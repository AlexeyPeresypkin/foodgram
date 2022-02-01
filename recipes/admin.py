from django.contrib import admin
from django.contrib.auth import get_user_model

from recipes.models import Recipe, Follow, Ingridient, RecipeIngredient, Tags, \
    Favorite, ShopList

User = get_user_model()


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', )
    list_filter = ('author', 'title', 'tags')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('author', 'user')


@admin.register(Ingridient)
class IngridientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingridient', 'quantity')


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')


@admin.register(ShopList)
class ShopListAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
