from django.db import models
from grocery_list.models import GroceryList


class GroceryListItem(models.Model):
    MEASUREMENT_UNITS = [
        ("Unit", "Unit"),
        ("Kilogram", "Kilogram"),
        ("Gram", "Gram"),
    ]

    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(null=True, blank=True)
    rate_measurement_quantity = models.FloatField()
    rate_measurement_unit = models.CharField(max_length=8, choices=MEASUREMENT_UNITS)
    rate = models.FloatField()
    quantity_measurement_unit = models.CharField(
        max_length=8, choices=MEASUREMENT_UNITS
    )
    quantity = models.FloatField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grocery_list = models.ForeignKey(
        GroceryList, on_delete=models.CASCADE, related_name="items"
    )

    def __str__(self):
        return self.name
