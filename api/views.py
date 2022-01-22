from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from recipes.models import Recipe, Favorite, Follow

from api.serializers import FavoriteSerializer, FollowSerializer

User = get_user_model()


class FavoriteCreateApiView(CreateAPIView):
    serializer_class = FavoriteSerializer


class FavoriteDeleteAPIView(DestroyAPIView):
    serializer_class = FavoriteSerializer
    queryset = Recipe.objects.all()

    def destroy(self, request, *args, **kwargs):
        Favorite.objects.filter(
            user=self.request.user, recipe=self.get_object()
        ).delete()
        return Response({"success": True})


class FollowCreateApiView(CreateAPIView):
    serializer_class = FollowSerializer


class FollowDeleteAPIView(DestroyAPIView):
    serializer_class = FollowSerializer
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        Follow.objects.filter(
            user=self.request.user, author=self.get_object()
        ).delete()
        return Response({"success": True})
