from rest_framework import serializers

from .models import ListProduct


class ListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListProduct
        
        fields = "__all__"
