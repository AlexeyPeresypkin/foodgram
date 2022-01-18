from django.urls import reverse_lazy

from .models import Tags, ShopList


class RecipeMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favorites = self.request.user.favorites.all().\
            values_list('recipe_id', flat=True)
        context['favorites'] = favorites
        return context
