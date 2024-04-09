from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import GroceryListItem
from .serializers import GroceryListItemSerializer


class GroceryListItemModelViewSet(viewsets.ModelViewSet):
    queryset = GroceryListItem.objects.all()

    permission_classes = [IsAuthenticated]

    serializer_class = GroceryListItemSerializer

    @extend_schema(
        request=GroceryListItemSerializer,
        responses={201: GroceryListItemSerializer()},
    )
    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id

        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={200: GroceryListItemSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        queryset = GroceryList.objects.filter(user=request.user)

        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)
