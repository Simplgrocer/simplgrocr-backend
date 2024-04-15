from rest_framework import serializers

from grocery_list_item.serializers import GroceryListItemSerializer

from .models import GroceryList


class GroceryListSerializer(serializers.ModelSerializer):
    items = GroceryListItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = GroceryList
        
        fields = "__all__"
