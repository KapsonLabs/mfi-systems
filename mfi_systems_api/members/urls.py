from django.urls import path, include
from . import views

urlpatterns = [
    path('institutions/groups/', views.GroupList.as_view(), name="loan-groups"),
    path('institutions/groups/<int:pk>/', views.GroupDetail.as_view(), name="loan-groups-detail"),
    path('clients/', views.UserClientCreate.as_view(), name="loan-clients"),
    path('clients/<int:pk>/', views.UserDetail.as_view(), name="loan-details"),
    path('institutions/groups/members/', views.MemberList.as_view(), name="group-members"),
    path('institutions/groups/members/<int:pk>/', views.MemberDetail.as_view(), name="group-members-detail"),
    path('institutions/groups/<int:pk>/memberfeestopay/', views.MemberFeesPayment.as_view(), name="group-member-fees-to-pay"),
    path('groups/<int:pk>/members/', views.GroupMemberList.as_view(), name="groups-members-list"),
]