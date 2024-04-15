from rest_framework.viewsets import ModelViewSet
from .models import GroceryListItem
from .serializers import GroceryListItemSerializer

class GroceryListItemViewSet(ModelViewSet):
    queryset = GroceryListItem.objects.all()
    serializer_class = GroceryListItemSerializer