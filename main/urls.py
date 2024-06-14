from django.urls import path
from . import views

urlpatterns = [
    path('', views.uploadImage, name="uploadImage"),
    path('processImage', views.processImage, name="processImage"),
    path('submit', views.submit, name="submit"),
    path('fix', views.fix, name="fix"),
    path('updateQuantity', views.updateQuantity, name="updateQuantity"),
    path('download/<filepath>', views.download_file, name='download_file'),
    path('source/<filepath>', views.source_file, name='source_file'),
]


