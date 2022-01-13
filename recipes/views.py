from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from foodgram.settings import PAGINATE_COUNT
from recipes.forms import RecipeForm
from recipes.models import Recipe

User = get_user_model()


class RecipesListView(ListView):
    paginate_by = PAGINATE_COUNT
    model = Recipe
    template_name = 'index.html'
    context_object_name = 'recipes'
    queryset = Recipe.objects.all(). \
        select_related('author'). \
        prefetch_related('tags')


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'


class RecipesByAuthor(ListView):
    template_name = 'recipes_by_author.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        author = get_object_or_404(User, pk=self.kwargs['pk'])
        return Recipe.objects.filter(author=author). \
            select_related('author'). \
            prefetch_related('tags')


class RecipesFollow(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes_follow.html'
    context_object_name = 'authors'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['pk'])
        # user = self.request.user
        follows = user.follower.all().values_list('author_id', flat=True)
        authors = User.objects.filter(id__in=list(follows))
        return authors


def recipe_create(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    post = request.POST
    print(post)
    post_items = request.POST.items()
    for k, v in post_items:
        print(k, v)
    # print(dir(request))
    # print(request.user)
    # print(post['time_cooking'])
    if form.is_valid():
        return render(request, 'recipe_create.html', context={'form': form})
    return render(request, 'recipe_create.html', context={'form': form})


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
