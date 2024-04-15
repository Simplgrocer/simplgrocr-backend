from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import GroceryList
from .serializers import GroceryListSerializer


class GroceryListViewSet(ModelViewSet):
    queryset = GroceryList.objects.all()
    serializer_class = GroceryListSerializer
    permission_classes = [IsAuthenticated]
