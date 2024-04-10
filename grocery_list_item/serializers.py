from rest_framework import serializers

from .models import GroceryListItem


class GroceryListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroceryListItem
        
        fields = "__all__"
