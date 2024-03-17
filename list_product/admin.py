from django.contrib import admin

from .models import ListProduct, MeasurementUnit


admin.site.register(MeasurementUnit)
admin.site.register(ListProduct)
