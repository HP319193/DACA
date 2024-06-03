from django.urls import path
from . import views

urlpatterns = [
    path('', views.uploadImage, name="uploadImage"),
    path('processImage', views.processImage, name="processImage"),
    path('submit', views.submit, name="submit"),
    path('download/<filepath>', views.download_file, name='download_file'),
]


