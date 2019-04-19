from django.urls import path, include
from . import views

urlpatterns = [
    path('institutions/', views.InstitutionList.as_view(), name="institutions"),
    path('institutions/institution_settings/', views.InstitutionSettingsList.as_view(), name="institution_settings"),
]