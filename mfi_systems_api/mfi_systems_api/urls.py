"""mfi_systems_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from accounts.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('api/v1/', include('members.urls'), name="member-routes"),
    path('api/v1/', include('loans_management.urls'), name="loans-routes"),
    path('api/v1/', include('mfi_statistics.urls'), name="mfi-statistics-routes"),
    path('api/v1/', include('institution.urls'), name="institution-routes"),
]
