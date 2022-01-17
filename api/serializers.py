from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('recipe', )

