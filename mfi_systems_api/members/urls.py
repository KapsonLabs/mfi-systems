from django.urls import path, include
from . import views

urlpatterns = [
    path('groups/', views.GroupList.as_view(), name="loan-groups"),
    path('groups/<int:pk>/', views.GroupDetail.as_view(), name="loan-groups-detail"),
    path('clients/', views.UserClientCreate.as_view(), name="loan-clients"),
    path('members/', views.MemberList.as_view(), name="group-members"),
    path('members/<int:pk>/', views.MemberDetail.as_view(), name="group-members-detail"),
    path('groups/<int:pk>/members/', views.GroupMemberList.as_view(), name="groups-members-list"),
]