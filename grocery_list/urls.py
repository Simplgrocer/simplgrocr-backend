from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("grocery-list", views.GroceryListModelViewSet, basename="grocery_list")

urlpatterns = [
    path("", include(router.urls)),
]
