from django.db import models
from accounts.models import User
from members.models import GroupMember

from django.core.validators import RegexValidator

class Loans(models.Model):
    """
    Loans model
    """
    loan_applicant              = models.ForeignKey(GroupMember, on_delete=models.CASCADE, related_name='member_group')
    responsible_loan_officer    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responsible_officer', null=True, blank=True)
    principal_amount            = models.DecimalField(max_digits=20, decimal_places=3)
    interest_rate               = models.DecimalField(max_digits=20,decimal_places=3, null=True, blank=True)
    loan_type                   = models.CharField(max_length=25)#[Small Loan, Small Business Loan],
    loan_disbursement_date      = models.DateField(blank=True, null=True)
    first_repayment_date        = models.DateField(blank=True, null=True) #//optional in some cases
    next_payment_date           = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    guarantor1                  = models.ForeignKey(GroupMember, on_delete=models.CASCADE, null=True, blank=True, related_name='loan_guarantor_1')
    guarantor2                  = models.ForeignKey(GroupMember, on_delete=models.CASCADE, null=True, blank=True, related_name='loan_guarantor_2')
    expected_income_corebznss   = models.CharField(max_length=20, null=False, blank=False,validators=[RegexValidator(r'(^[0-9+-]+$)')])  
    expected_profit_corebznss   = models.CharField(max_length=20, null=False, blank=False,validators=[RegexValidator(r'(^[0-9+-]+$)')])  
    corebznss_comment           = models.CharField(max_length=200, null=True, blank=True)
    loan_cycle_frequency        = models.CharField(max_length=10) #//must be of [Weekly, Monthly]
    expected_duration           = models.CharField(max_length=6, blank=False, null=False)
    loan_insurance_fee          = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    loan_processing_fee         = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True) #// must be of length [9]
    loan_balance_to_pay         = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    loan_purpose                = models.CharField(max_length=25)
    loan_cycle                  = models.CharField(max_length=200, null=True, blank=True)
    loan_completed              = models.BooleanField(default=False)
    loan_status                 = models.BooleanField(default=False)
    is_loan_disbursed           = models.BooleanField(default=False)
    loan_completed_date         = models.DateTimeField(blank=True, null=True)
    timestamp                   = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} Loan belongs to {} member".format(self.principal_amount, self.loan_applicant)

class LoanApproval(models.Model):
    """
    Loan Approval Model
    """
    approved_by     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approval_officer')
    approved_loan   = models.ForeignKey(Loans, on_delete=models.CASCADE, related_name='loan_approved')
    date_approved   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} Loan approved by {} member".format(self.approved_loan, self.approved_by)


class LoanDisbursal(models.Model):
    """
    Loan Disbursal Model
    """
    disbursed_by     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disbursal_officer')
    disbursed_loan   = models.ForeignKey(Loans, on_delete=models.CASCADE, related_name='loan_disbursed')
    date_disbursed   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} Loan disbursed by {} member".format(self.disbursed_loan, self.disbursed_by)


class LoanCycles(models.Model):
    """
    Loan Cycles Model
    """
    related_loan        = models.ForeignKey(Loans, on_delete=models.CASCADE, null=False, blank=False, related_name='related_loan_for_cycle')
    cycle_date          = models.DateTimeField(auto_now_add=False)
    cycle_status        = models.CharField(max_length=100, null=False, blank=False, default="Unpaid")
    amount_expected     = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True) 
    amount_paid         = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True) 
    balance             = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    loan_balance        = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)


class LoanPayments(models.Model):
    """
    Loan Payments Model
    """ 
    related_loan_cycle  = models.ForeignKey(LoanCycles, on_delete=models.CASCADE, null=False, blank=False)
    amount_paid         = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    received_by         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_confirmation_officer', null=True, blank=True) 
    balance             = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)  
    fined_amount        = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    comment             = models.TextField()
    date_paid           = models.DateField(auto_now_add=False)
    timestamp           = models.DateTimeField(auto_now_add=True)

