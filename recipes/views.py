from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from recipes.forms import RecipeForm
from recipes.models import Recipe

User = get_user_model()


class RecipesListView(ListView):
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
        user = self.request.user
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


# @login_required
# def follow_index(request):
#     # информация о текущем пользователе доступна в переменной request.user
#     posts = Post.objects.filter(author__following__user=request.user).order_by(
#         '-pub_date')
#     paginator = Paginator(posts, 10)
#     # показывать по 10 записей на странице.
#     page_number = request.GET.get(
#         'page')  # переменная в URL с номером запрошенной страницы
#     page = paginator.get_page(
#         page_number)  # получить записи с нужным смещением
#     return render(request, "follow.html",
#                   {'page': page, 'paginator': paginator})
