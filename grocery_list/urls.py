from django.urls import path, include
from rest_framework_nested import routers

from grocery_list_item.views import GroceryListItemViewSet

from . import views

router = routers.DefaultRouter()

router.register(r"grocery-lists", views.GroceryListViewSet)

grocery_list_router = routers.NestedSimpleRouter(
    router, r"grocery-lists", lookup="grocery_list"
)

grocery_list_router.register(
    r"items", GroceryListItemViewSet, basename="grocery-list-items"
)

urlpatterns = [
    path("", include("djoser.urls")),
    path("", include("djoser.urls.authtoken")),
    path("users/", include(router.urls)),
    path("users/", include(grocery_list_router.urls)),
]
