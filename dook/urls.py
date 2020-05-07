from django.http import HttpResponse
from django.urls import include, path

from dook.api.urls import url_patterns as api_url_patterns

urlpatterns = [
    path("", lambda r: HttpResponse()),
    path(r"^admin/", include(("dook.api.admin.urls", "admin"), namespace="admin")),
    path(r"^api/", include((api_url_patterns, "api"), namespace="api")),
    path(r"^users/", include(("dook.users.urls", "users"), namespace="users")),
]
