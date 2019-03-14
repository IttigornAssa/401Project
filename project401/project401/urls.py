from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from myapp.models import changeReq
from django.conf.urls import url, include
from myapp.urls import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.demoDatabases, name='demoDatabases'),
    path(r'api/', include(router.urls))
]
