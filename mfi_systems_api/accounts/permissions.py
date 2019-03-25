from rest_framework.permissions import BasePermission
from .models import User

class BranchManagerPermissions(BasePermission):
    allowed_user_roles = (User.is_branch_manager, User.is_active)

    def has_permission(self, request, view):
        is_allowed_user = request.user in self.allowed_user_roles
        return is_allowed_user

class LoanOfficerPermissions(BasePermission):
    allowed_user_roles = (User.is_loan_officer, User.is_active)

    def has_permission(self, request, view):
        is_allowed_user = request.user in self.allowed_user_roles
        return is_allowed_user

class LoanClientPermissions(BasePermission):
    allowed_user_roles = (User.is_client, User.is_active)

    def has_permission(self, request, view):
        is_allowed_user = request.user in self.allowed_user_roles
        return is_allowed_user