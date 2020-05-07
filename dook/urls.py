from django.http import HttpResponse
from django.urls import include, path

from dook.api.urls import url_patterns as api_url_patterns

urlpatterns = [
    path("", lambda r: HttpResponse()),
    path("admin/", include(("dook.admin.urls", "admin"), namespace="admin")),
    path("api/", include((api_url_patterns, "api"), namespace="api")),
    path("users/", include(("dook.users.urls", "users"), namespace="users")),
]
