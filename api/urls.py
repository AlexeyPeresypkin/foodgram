from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import recipe_list

router = DefaultRouter()
# router.register(r'favorites/', recipe_list)

urlpatterns = [
    path('', include(router.urls)),
    path('favorites', recipe_list)

]
