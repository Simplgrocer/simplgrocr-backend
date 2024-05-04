from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from grocery_list.models import GroceryList
from .models import GroceryListItem
from .serializers import GroceryListItemSerializer
from django.db import transaction


class GroceryListItemViewSet(ModelViewSet):
    serializer_class = GroceryListItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroceryListItem.objects.filter(
            grocery_list=self.kwargs["grocery_list_pk"]
        )

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.data["grocery_list"] = self.kwargs["grocery_list_pk"]

        response = super().create(request, *args, **kwargs)

        if response.status_code != 201:
            return response

        grocery_list = GroceryList.objects.get(pk=self.kwargs["grocery_list_pk"])

        grocery_list.total_price += request.data["price"]

        grocery_list.save()

        return response

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        if not request.data.get("price"):
            return super().update(request, *args, **kwargs)

        old_price = self.get_object()

        if old_price.price == request.data["price"]:
            return super().update(request, *args, **kwargs)

        grocery_list = old_price.grocery_list

        grocery_list.price = (
            grocery_list.total_price - old_price.price + request.data["price"]
        )

        grocery_list.save()

        return super().update(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)

        if not response.status_code == 204:
            return response
        
        grocery_list = self.get_object().grocery_list

        grocery_list.total_price -= self.get_object().price

        grocery_list.save()

