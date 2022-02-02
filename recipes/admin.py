from django.contrib import admin
from django.contrib.auth import get_user_model

from recipes.models import Recipe, Follow, Ingridient, RecipeIngredient, Tags, \
    Favorite, ShopList

User = get_user_model()


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ('title', 'author', 'favorite_count')
    list_filter = ('author', 'tags')
    search_fields = ('title', 'author__username',)
    readonly_fields = ('favorite_count',)
    prepopulated_fields = {'slug': ('title',)}

    @admin.display(description='Рецепт в избранном')
    def favorite_count(self, obj):
        return obj.favorites.count()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('author', 'user')


@admin.register(Ingridient)
class IngridientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    search_fields = ('title',)


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
