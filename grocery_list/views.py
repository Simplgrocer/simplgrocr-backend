from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import GroceryList
from .serializers import GroceryListSerializer
from grocery_list_item.serializers import GroceryListItemSerializer


class GroceryListModelViewSet(viewsets.ModelViewSet):
    queryset = GroceryList.objects.all()

    permission_classes = [IsAuthenticated]

    serializer_class = GroceryListSerializer

    @extend_schema(
        request=GroceryListSerializer,
        responses={201: GroceryListSerializer()},
    )
    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id

        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={200: GroceryListSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        queryset = GroceryList.objects.filter(user=request.user)

        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="product")
    @extend_schema(
        request=GroceryListItemSerializer,
        responses={201: GroceryListItemSerializer()},
    )
    def create_product(self, request, *args, **kwargs):
        serializer = GroceryListItemSerializer(data=request.data)
        if serializer.is_valid():
            # Extracting list id from request data
            list_id = request.data.get("list")
            try:
                list_instance = GroceryList.objects.get(id=list_id)
            except GroceryList.DoesNotExist:
                return Response(
                    {"error": "GroceryList does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Associate the current user with the list product
            serializer.validated_data["list"] = list_instance

            # Save the list product
            list_item = serializer.save()

            return Response(
                GroceryListItemSerializer(list_item).data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
