from django.urls import path, include
from . import views

urlpatterns = [
    path('institutions/<int:pk>/statistics/collections/', views.InstitutionStatisticsCollections.as_view(), name="mfi-statistics-savings"),
    path('institutions/statistics/loans/', views.StatisticsView.as_view(), name="mfi-statistics-loans"),
]