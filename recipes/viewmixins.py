from django.urls import reverse_lazy

from .models import Tags, ShopList


class RecipeMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favorites = self.request.user.favorites.all(). \
            values_list('recipe_id', flat=True)
        context['favorites'] = favorites
        return context


class TagsMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.getlist('tag')
        if q:
            return queryset.filter(tags__slug__in=q).distinct()
        return queryset
