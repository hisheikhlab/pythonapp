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
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
urlpatterns = [
    path('', views.default, name='defaultpage'),
    path('login/', views.log, name='login'),
    path('user/<str:user_id>/', views.todo, name='users'),
    path('logout/', views.logo, name='logout'),
    path('signup/', views.reg, name='signup'),
    path('activate/<str:new_id>/', views.activate, name='activate'),
    path('password_reset/', PasswordResetView.as_view(template_name='forget password.html'), name='password_reset'),
    path('password_change/', PasswordChangeView.as_view(template_name='change password.html', extra_context={'status':
                                                                                                             'change'}),
         name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='change password.html', extra_context={'status':
                                                                                                                  'done'}),
         name='password_change_done'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='forget password.html',
                                                               extra_context={'status': 'done'}),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='forget '
                                                                                                    'password.html',
                                                                                      extra_context={'status':
                                                                                                     'confirmed'}),
         name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='forget '
                                                                                     'password.html',
                                                                       extra_context={'status':
                                                                                          'completed'}),
         name='password_reset_complete'),

]
