from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response
from recipes.models import Recipe, Favorite, Follow, ShopList, Ingridient

from api.serializers import FavoriteSerializer, FollowSerializer, \
    ShopListSerializer, IngridientSerializer

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


class ShopListCreateApiView(CreateAPIView):
    serializer_class = ShopListSerializer


class ShopListDeleteAPIView(DestroyAPIView):
    serializer_class = ShopListSerializer
    queryset = Recipe.objects.all()

    def destroy(self, request, *args, **kwargs):
        ShopList.objects.filter(
            user=self.request.user, recipe=self.get_object()
        ).delete()
        return Response({"success": True})


class IngridientApiSerializer(ListAPIView):
    serializer_class = IngridientSerializer

    def get_queryset(self):
        queryset = Ingridient.objects.all()
        query = self.request.query_params.get('query')
        return queryset.filter(title__icontains=query)
