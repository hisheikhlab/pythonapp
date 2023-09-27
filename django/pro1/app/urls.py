"""
URL configuration for pro1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Import Django's auth views


urlpatterns = [
    path('', views.default, name='defaultpage'),
    path('login/', views.log, name='login'),
    path('user/<str:user_id>/', views.todo, name='users'),
    path('logout/', views.logo, name='logout'),
    path('signup/', views.reg, name='signup'),
    path('activate/<str:new_id>/', views.activate, name='activate'),
]


