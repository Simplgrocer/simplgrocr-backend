from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import GroceryList
from .serializers import GroceryListSerializer


class GroceryListViewSet(ModelViewSet):
    queryset = GroceryList.objects.all()
    serializer_class = GroceryListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroceryList.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data["user"] = request.user.id

        return super().update(request, *args, **kwargs)
