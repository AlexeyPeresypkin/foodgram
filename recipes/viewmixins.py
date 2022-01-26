from django.urls import reverse_lazy

from .models import Tags, ShopList


class RecipeMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            favorites = self.request.user.favorites.all(). \
                values_list('recipe_id', flat=True)
            shoplist = self.request.user.shop_list.all(). \
                values_list('recipe_id', flat=True)
            context['favorites'] = favorites
            context['shoplist'] = shoplist
        return context


class TagsMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.getlist('tag')
        if q:
            return queryset.filter(tags__slug__in=q).distinct()
        return queryset


class IsAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().author:
            return reverse_lazy("recipes:recipe", kwargs.get("pk"))
        return super().dispatch(request, *args, **kwargs)
