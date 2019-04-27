from rest_framework.permissions import BasePermission
from .models import User

class InstitutionAdministratorPermissions(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_institution_administrator and request.user.is_active

class InstitutionAdministratorAndLoanOfficerPermissions(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_institution_administrator or request.user.is_loan_officer and request.user.is_active

class BranchManagerPermissions(BasePermission):
    allowed_user_roles = (User.is_branch_manager, User.is_active)

    def has_permission(self, request, view):
        is_allowed_user = request.user in self.allowed_user_roles
        return is_allowed_user

class LoanOfficerPermissions(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_loan_officer and request.user.is_active

class LoanClientPermissions(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_client and request.user.is_active