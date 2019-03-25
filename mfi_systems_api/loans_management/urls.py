from django.urls import path, include
from . import views

urlpatterns = [
    path('loans/', views.LoansList.as_view(), name="loans"),
    path('loans/<int:pk>/status/', views.LoansStatus.as_view(), name="loans_status"),
    path('loans/<int:pk>/status/update/', views.LoanStatusUpdate.as_view(), name="loans_status_update"),
    path('loans/<int:pk>/status/disburse/', views.LoanDisbursement.as_view(), name="loans_disbursement"),
]