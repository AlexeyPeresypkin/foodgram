from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True, source='user.username')

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
