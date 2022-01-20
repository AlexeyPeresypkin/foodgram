from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from foodgram.settings import PAGINATE_COUNT
from recipes.forms import RecipeForm
from recipes.models import Recipe, Tags
from recipes.viewmixins import RecipeMixin, TagsMixin

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
        queryset.filter(author=author)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, id=self.kwargs.get('pk'))
        context['author'] = author
        return context


class RecipeDetailView(RecipeMixin, DetailView):
    model = Recipe
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'


class RecipesFollow(LoginRequiredMixin, ListView):
    paginate_by = PAGINATE_COUNT
    model = Recipe
    template_name = 'recipes_follow.html'
    context_object_name = 'authors'

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs.get('pk'))
        # user = self.request.user
        follows = user.follower.all().values_list('author_id', flat=True)
        authors = User.objects.filter(id__in=list(follows)).order_by('-id')
        return authors


class RecipesFavorite(LoginRequiredMixin, ListView):
    paginate_by = PAGINATE_COUNT
    model = Recipe
    template_name = 'recipes_favorite.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs.get('pk'))
        favorites = user.favorites.values_list('recipe_id', flat=True)
        recipes = Recipe.objects.filter(id__in=list(favorites))
        return recipes


def recipe_create(request):
    form = RecipeForm()
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        print(form.is_valid())
        print(form.cleaned_data)
        # print(list((request.POST).items()))
        print(request.POST)
        if form.is_valid():
            return render(request, 'recipe_create.html', {'form': form})
    return render(request, 'recipe_create.html', {'form': form})

    # form = RecipeForm(request.POST or None, files=request.FILES or None)
    # post = request.POST
    # print(post)
    # # print(form)
    # post_items = request.POST.items()
    # for k, v in post_items:
    #     print(k, v)
    # # print(dir(request))
    # # print(request.user)
    # # print(post['time_cooking'])
    # if form.is_valid():
    #     return render(request, 'recipe_create.html', context={'form': form})
    # return render(request, 'recipe_create.html', context={'form': form})


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
