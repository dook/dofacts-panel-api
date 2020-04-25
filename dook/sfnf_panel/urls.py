"""sfnf-panel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.http import HttpResponse
from django.urls import include, path

from dook.api.urls import url_patterns as api_url_patterns

urlpatterns = [
    path("", lambda r: HttpResponse()),
    path("admin/", include(("dook.admin.urls", "admin"), namespace="admin")),
    path("api/", include((api_url_patterns, "api"), namespace="api")),
    path("users/", include(("dook.users.urls", "users"), namespace="users")),
]
