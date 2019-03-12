from django.urls import path, include
from . import views

urlpatterns = [
    path('groups/<int:pk>/', views.LoanGroupRudView.as_view(), name="loan-groups"),
]