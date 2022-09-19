from django.conf.urls.static import static
from django.urls import path, re_path
from . import views
    
urlpatterns = [
      path("", views.DefaultTemplateView.as_view(), name='health'),
]