from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls)
]
