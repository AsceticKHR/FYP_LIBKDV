
from . import views
from django.urls import path
from .views import upload_file


urlpatterns = [
    path('', views.index),
    path('api/upload/', upload_file),
]