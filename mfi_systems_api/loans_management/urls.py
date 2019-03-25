from django.urls import path, include
from . import views

urlpatterns = [
    path('loans/', views.LoansList.as_view(), name="loans"),
    path('loans/<int:pk>/status/', views.LoansStatus.as_view(), name="loans_status"),
]