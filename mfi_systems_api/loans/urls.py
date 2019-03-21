from django.urls import path, include
from . import views

urlpatterns = [
    path('groups/', views.GroupList.as_view(), name="loan-groups"),
]