from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


prefix = "api/v1/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        prefix,
        include(
            [
                path("schema/", SpectacularAPIView.as_view(), name="schema"),
                path(
                    "schema/swagger-ui/",
                    SpectacularSwaggerView.as_view(url_name="schema"),
                    name="swagger-ui",
                ),
                path(
                    "schema/redoc/",
                    SpectacularRedocView.as_view(url_name="schema"),
                    name="redoc",
                ),
                path("", include("grocery_list.urls")),
                # path("", include("list_item.urls")),
                path("", include("user.urls")),
            ]
        ),
    ),
]
