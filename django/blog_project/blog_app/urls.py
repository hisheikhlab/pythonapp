"""
URL configuration for blog_project project.

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
from django.urls import path, include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.default, name='default'),
    path('add/', views.add, name='add'),
    path('delete/', views.delete, name='delete'),
    path('login/', views.log, name='login'),
    path('logout/', views.logou, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('home/<str:user_id>/', views.home, name='home'),
    path('blog/<int:blog_id>/', views.blog, name='blog'),
    path('search/', views.search, name='search'),
]
