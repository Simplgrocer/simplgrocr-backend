from rest_framework.viewsets import ModelViewSet
from .models import GroceryList
from .serializers import GroceryListSerializer


class GroceryListViewSet(ModelViewSet):
    queryset = GroceryList.objects.all()
    serializer_class = GroceryListSerializer
