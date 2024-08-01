from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add, name="addmember"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('update/<int:id>', views.update, name="update"),
    path('update/memberupdate/<int:id>', views.updatemember, name="updatemember"),
    path("add/addrecord/", views.addrecord, name="addrecord"),
    path('', views.uploadImage, name="uploadImage"),
    path('processImage', views.processImage, name="processImage"),
    path('adminProcess', views.adminProcess, name="admin"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('handlelogin/', views.handlelogin, name="handlelogin"),
    path('submit', views.submit, name="submit"),
    path('fix', views.fix, name="fix"),
    path('recheck', views.recheck, name="recheck"),
    path('updateQuantity', views.updateQuantity, name="updateQuantity"),
    path('processFix', views.processFix, name="processFix"),
    path('download/<filepath>', views.download_file, name='download_file'),
    path('source/<filepath>', views.source_file, name='source_file'),
]


