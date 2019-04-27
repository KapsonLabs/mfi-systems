from django.urls import path, include
from . import views

urlpatterns = [
    path('institutions/', views.InstitutionList.as_view(), name="institutions"),
    path('institutions/<int:pk>/', views.InstitutionDetail.as_view(), name="institution_detail"),
    path('institutions/institution_settings/', views.InstitutionSettingsList.as_view(), name="institution_settings"),
    path('institutions/institution_settings/<int:pk>/', views.InstitutionSettingsDetail.as_view(), name="institution_settings_detail"),
]