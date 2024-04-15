from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import GroceryListItem
from .serializers import GroceryListItemSerializer

class GroceryListItemViewSet(ModelViewSet):
    serializer_class = GroceryListItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroceryListItem.objects.filter(grocery_list=self.kwargs['grocery_list_pk'])