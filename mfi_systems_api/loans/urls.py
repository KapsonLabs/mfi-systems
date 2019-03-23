from django.urls import path, include
from . import views

urlpatterns = [
    path('loans/', views.LoanList.as_view(), name="loans"),
]