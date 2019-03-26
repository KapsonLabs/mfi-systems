from django.urls import path, include
from . import views

urlpatterns = [
    path('statistics/', views.StatisticsView.as_view(), name="mfi-statistics"),
]