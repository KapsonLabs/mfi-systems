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
    path('institutions/groups/<int:pk>/members/', views.GroupMemberList.as_view(), name="groups-members-list"),
    path('institutions/groups/<int:pk>/members/savingstopay/', views.SavingsToBePaid.as_view(), name='group-savings-to-be-paid'),
    path('institutions/groups/members/saving_accounts/', views.SavingsAccountList.as_view(), name='savings-account-lists'),
    path('institutions/groups/members/savings/', views.SavingsPaymentList.as_view(), name="members-savings-list"),
    path('institutions/groups/members/savings_withdraw/', views.SavingsWithdrawal.as_view(), name="members-savings-withdraw"),
]