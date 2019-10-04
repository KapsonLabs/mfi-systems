from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_institution_administrator = models.BooleanField(default=False)
    is_loan_officer = models.BooleanField(default=False)
    is_loan_manager = models.BooleanField(default=False)
    is_teller = models.BooleanField(default=False)
    is_branch_manager = models.BooleanField(default=False)
    is_asst_branch_manager = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)