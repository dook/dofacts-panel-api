from django.http import HttpResponse
from django.urls import include, path

urlpatterns = [
    path("", lambda r: HttpResponse()),
    path(r"^admin/", include(("dook.api.admin.urls", "admin"), namespace="admin")),
    path(r"^api/", include(("dook.api.news.urls", "api"), namespace="api")),
    path(r"^users/", include(("dook.users.urls", "users"), namespace="users")),
]
