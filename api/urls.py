from django.urls import path

from api.views import FavoriteCreateApiView, FavoriteDeleteAPIView, \
    FollowCreateApiView, FollowDeleteAPIView, ShopListCreateApiView, \
    ShopListDeleteAPIView, IngridientApiSerializer

urlpatterns = [
    path('favorites', FavoriteCreateApiView.as_view()),
    path('favorites/<int:pk>', FavoriteDeleteAPIView.as_view()),
    path('subscriptions', FollowCreateApiView.as_view()),
    path('subscriptions/<int:pk>', FollowDeleteAPIView.as_view()),
    path('purchases', ShopListCreateApiView.as_view()),
    path('purchases/<int:pk>', ShopListDeleteAPIView.as_view()),
    path('ingredients', IngridientApiSerializer.as_view()),

]
