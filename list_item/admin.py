from django.contrib import admin

from .models import ListItem, MeasurementUnit


admin.site.register(MeasurementUnit)
admin.site.register(ListItem)
