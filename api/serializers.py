from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import Favorite, Recipe, Follow

User = get_user_model()


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        slug_field="id", queryset=Recipe.objects.all(), source="recipe"
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorite
        fields = ('id', 'user')


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        slug_field='id', queryset=User.objects.all(), source='author'
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Follow
        fields = ('id', 'user')

