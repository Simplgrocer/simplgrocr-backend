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

    @action(detail=True, methods=["post"], url_path="item")
    @extend_schema(
        request=GroceryListItemSerializer,
        responses={201: GroceryListItemSerializer()},
    )
    def create_grocery_list_item(self, request, *args, **kwargs):
        grocery_list = get_object_or_404(GroceryList, pk=kwargs["pk"])

        if not grocery_list.user == request.user:
            return Response(
                {"error": "You are not authorized to perform this action."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        request.data["grocery_list"] = kwargs["pk"]

        serializer = GroceryListItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=["post"], url_path="items")
    @extend_schema(
        request=GroceryListItemSerializer,
        responses={201: GroceryListItemSerializer()},
    )
    def create_grocery_list_items(self, request, *args, **kwargs):
        grocery_list = get_object_or_404(GroceryList, pk=kwargs["pk"])

        if not grocery_list.user == request.user:
            return Response(
                {"error": "You are not authorized to perform this action."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        for item in request.data:
            item["grocery_list"] = kwargs["pk"]

        serializer = GroceryListItemSerializer(data=request.data, many=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
