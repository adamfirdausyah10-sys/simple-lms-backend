from django.contrib import admin
from django.http import JsonResponse
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", lambda request: JsonResponse({"status": "ok"})),
]
