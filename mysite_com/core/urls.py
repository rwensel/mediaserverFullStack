from django.contrib import admin
from django.urls import include, re_path, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("health/", include("health.urls"), name="health"),
    path("", include("home.urls"), name="home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)