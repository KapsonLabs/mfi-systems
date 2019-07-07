from django.urls import path, include
from .views import LoginView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name="auth-login"),
]