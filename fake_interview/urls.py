from django.contrib import admin
from django.urls import path
from detection import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home),
    path('test/', views.test_api),

    path('start/', views.start_detection),
    path('stop/', views.stop_detection),

    path('register/', views.register),
    path('login/', views.login),
]