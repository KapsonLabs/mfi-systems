from django.db import models
from accounts.models import User

from django.core.validators import RegexValidator
from .choices import FREQUENCY, ROLES, LOAN_CALCULATORS, INTEREST_CALCULATORS, LOAN_TYPES, INSTITUTION_TYPE

class Institution(models.Model):

    created_by                      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='institution_creator')
    institution_name                = models.CharField(max_length=250)
    institution_type                = models.CharField(max_length=25, choices=INSTITUTION_TYPE)
    location                        = models.CharField(max_length=25)
    certificate_of_incoporation     = models.ImageField(upload_to='institutions/', blank=True, null=True)
    date_of_incoporation            = models.DateField(auto_now_add=False, blank=True, null=True)
    date_created                    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.institution_name

class InstitutionSettings(models.Model):

    institution_id                 = models.OneToOneField(Institution, on_delete=models.CASCADE, related_name='institution_related')
    membership_fee                 = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    membership_fee_frequency       = models.CharField(max_length=20, blank=True, null=True, choices=FREQUENCY)
    share_price                    = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    minimum_shares                 = models.IntegerField()
    maximum_shares                 = models.IntegerField()
    savings_amount                 = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    savings_frequency              = models.CharField(max_length=20, blank=True, null=True, choices=FREQUENCY)
    savings_interest               = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    savings_interest_calculator    = models.CharField(max_length=20, blank=True, null=True, choices=INTEREST_CALCULATORS)
    savings_interest_frequency     = models.CharField(max_length=20, blank=True, null=True, choices=FREQUENCY)
    maximum_savings_to_withdraw    = models.DecimalField(max_digits=20, decimal_places=3 ,default=100)
    maximum_monthly_withdraws      = models.IntegerField(default=0)
    loan_types_provided            = models.CharField(max_length=15, blank=True, null=True, choices=LOAN_TYPES) 
    quick_loan_interest_rate       = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    small_loan_interest_rate       = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    big_loan_interest_rate         = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    quick_loan_limit               = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    quick_loan_repayment_limit     = models.IntegerField(default=0) #in months
    percentage_of_savings_rq_loan  = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    loan_interest_rate             = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    small_loan_interest_calculator = models.CharField(max_length=20, blank=True, null=True, choices=LOAN_CALCULATORS)
    quick_loan_interest_calculator = models.CharField(max_length=20, blank=True, null=True, choices=LOAN_CALCULATORS)
    big_loan_interest_calculator   = models.CharField(max_length=20, blank=True, null=True, choices=LOAN_CALCULATORS)
    loan_guarantors_required       = models.IntegerField()
    loan_processing_fee_percentage = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    loan_insurance_fee_percentage  = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    date_created                   = models.DateTimeField(auto_now_add=True)

class InstitutionStaff(models.Model):

    user_id                        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='institution_user')
    institution_id                 = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='institution_staff')
    staff_name                     = models.CharField(max_length=25)
    staff_role                     = models.CharField(max_length=20, blank=True, null=True, choices=ROLES)
    staff_responsibility           = models.TextField()
    date_created                   = models.DateTimeField(auto_now_add=True)
