"""foodgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from recipes.views import (
    RecipesListView,
    RecipeDetailView,
    RecipesByAuthor,
    RecipesFollow,
    RecipesFavorite,
    ShopListView,
    RecipeCreateView,
    RecipeEditView,
    RecipeDeleteView,
    RecipeShopItemDeleteView,
    ShopListDownloadView,

)

urlpatterns = [
    path(
        '',
        RecipesListView.as_view(),
        name='index'
    ),
    path(
        'recipe/<int:pk>/',
        RecipeDetailView.as_view(),
        name='recipe_detail'
    ),
    path(
        'recipe/follow/<int:pk>',
        RecipesFollow.as_view(),
        name='recipes_follow'
    ),
    path(
        'recipe/new/',
        RecipeCreateView.as_view(),
        name='recipe_create'
    ),
    path(
        'recipe/edit/<int:pk>/',
        RecipeEditView.as_view(),
        name='recipe_edit'
    ),
    path(
        'recipe/delete/<int:pk>/',
        RecipeDeleteView.as_view(),
        name='recipe_delete'
    ),
    path(
        'author/<int:pk>/',
        RecipesByAuthor.as_view(),
        name='recipes_by_author'
    ),
    path(
        'favirite/<int:pk>/',
        RecipesFavorite.as_view(),
        name='recipes_favorite'
    ),
    path(
        'shoplist/<int:pk>/',
        ShopListView.as_view(),
        name='shop_list'
    ),
    path(
        'shoplist/<int:pk>/delete/<int:recipe_id>',
        RecipeShopItemDeleteView.as_view(),
        name='shop_list_delete_item'
    ),
    path(
        'shoplist/<int:pk>/download',
        ShopListDownloadView.as_view(),
        name='shop_list_download'
    ),
]
