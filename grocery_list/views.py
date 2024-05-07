from io import BytesIO
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from common.utils.env import get_env_vars
from .utils import generate_grocery_list_summary
from .models import GroceryList
from .serializers import GroceryListSerializer
from rest_framework.response import Response
from django.core.files import File
from django.http import FileResponse


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

    @action(detail=True, methods=["get"])
    def summary(self, request, pk):
        grocery_list = self.get_object()
        grocery_list_items = grocery_list.items.all()

        grocery_list_items_list = [
            (
                "Name",
                "Description",
                "Rate Measurement Quantity",
                "Rate Measurement Unit",
                "Rate",
                "Quantity Measurement Unit",
                "Quantity",
                "Price"
            )
        ]

        for grocery_list_item in grocery_list_items:
            grocery_list_items_list.append(
                (
                    grocery_list_item.name,
                    grocery_list_item.description,
                    str(grocery_list_item.rate_measurement_quantity),
                    grocery_list_item.rate_measurement_unit,
                    str(grocery_list_item.rate),
                    grocery_list_item.quantity_measurement_unit,
                    str(grocery_list_item.quantity),
                    str(grocery_list_item.price),
                )
            )

        output = generate_grocery_list_summary(
            grocery_list.name,
            grocery_list.total_price,
            grocery_list_items_list,
            grocery_list.description,
        )

        bytes_io = BytesIO(output)

        summary_file = File(bytes_io)

        return FileResponse(summary_file, content_type="application/pdf")
