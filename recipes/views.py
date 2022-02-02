import csv

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView

from foodgram.settings import PAGINATE_COUNT
from recipes.forms import RecipeForm
from recipes.models import Recipe, Tags, ShopList
from recipes.viewmixins import RecipeMixin, TagsMixin, IsAuthorMixin

User = get_user_model()


class RecipesListView(RecipeMixin, TagsMixin, ListView):
    paginate_by = PAGINATE_COUNT
    model = Recipe
    template_name = 'index.html'
    context_object_name = 'recipes'
    queryset = Recipe.objects.all(). \
        select_related('author'). \
        prefetch_related('tags')
    extra_context = {'tags': Tags.objects.all()}


class RecipesByAuthor(RecipesListView):
    template_name = 'recipes_by_author.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        author = get_object_or_404(User, id=self.kwargs.get('pk'))
        queryset = queryset.filter(author=author)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, id=self.kwargs.get('pk'))
        follower_list = self.request.user. \
            follower.values_list('author_id', flat=True)
        context['author'] = author
        context['follower_list'] = follower_list
        return context


class RecipesFavorite(RecipesListView, LoginRequiredMixin):
    model = Recipe
    template_name = 'recipes_favorite.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = get_object_or_404(User, id=self.kwargs.get('pk'))
        favorites = user.favorites.values_list('recipe_id', flat=True)
        queryset = queryset.filter(id__in=list(favorites))
        return queryset


class RecipesFollow(LoginRequiredMixin, ListView):
    paginate_by = PAGINATE_COUNT
    model = Recipe
    template_name = 'recipes_follow.html'
    context_object_name = 'authors'

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs.get('pk'))
        follows = user.follower.all().values_list('author_id', flat=True)
        authors = User.objects.filter(id__in=list(follows)).order_by('-id')
        return authors


class ShopListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'shopList.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs.get('pk'))
        shop_list = user.shop_list.all().values_list('recipe_id', flat=True)
        recipes = Recipe.objects.filter(id__in=list(shop_list))
        return recipes


class RecipeDetailView(RecipeMixin, DetailView):
    model = Recipe
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = 'recipe_create.html'
    form_class = RecipeForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})


class RecipeEditView(IsAuthorMixin, LoginRequiredMixin, UpdateView):
    model = Recipe
    template_name = 'recipe_change.html'
    form_class = RecipeForm

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})


class RecipeDeleteView(LoginRequiredMixin, IsAuthorMixin, DeleteView):
    model = Recipe
    success_url = 'index'
    template_name = 'recipe_confirm_delete.html'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("index")


class RecipeShopItemDeleteView(LoginRequiredMixin, DeleteView):
    model = ShopList

    def get_object(self, queryset=None):
        user = User.objects.get(pk=self.kwargs.get('pk'))
        recipe = Recipe.objects.get(pk=self.kwargs.get('recipe_id'))
        print(recipe)
        print(user)
        obj = get_object_or_404(ShopList, user__id=user.id,
                                recipe__id=recipe.id)
        return obj

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy("shop_list", kwargs={'pk': pk})


class ShopListDownloadView(View):
    def get(self, request, *args, **kwargs):
        ingredients = Recipe.objects.values(
            'ingridients__title', 'ingridients__dimension'
        ) \
            .filter(shop_list__user=self.request.user) \
            .annotate(Sum('recipe_ingridient__quantity')) \
            .order_by('ingridients__title')
        response = HttpResponse(
            content_type='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename="shop_list.csv"'},
        )
        writer = csv.writer(response, delimiter=';')
        writer.writerow(['Ингридиент', 'Кол-во', 'Единица измерения'])
        for ingredient in ingredients:
            writer.writerow([
                ingredient['ingridients__title'],
                ingredient['recipe_ingridient__quantity__sum'],
                ingredient['ingridients__dimension'],
            ])
        return HttpResponse(response)


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
