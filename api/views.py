from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipes.models import Recipe, Favorite

from api.serializers import FavoriteSerializer


@api_view(['GET', 'POST'])
def recipe_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Favorite.objects.all()
        serializer = FavoriteSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data)
        serializer = FavoriteSerializer(data=request.data)
        return Response({"success": 'false'})
