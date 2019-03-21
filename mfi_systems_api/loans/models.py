from django.db import models
from accounts.models import User
from members.models import GroupMember

class Loan(models.Model):
    """
    Loan model
    """
    loan_applicant              = models.ForeignKey(GroupMember, on_delete=models.CASCADE, related_name='member_group')
    responsible_loan_officer    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responsible_officer')
    principal_amount            = models.DecimalField(max_digits=20, decimal_places=3)
    interest_rate               = models.DecimalField(max_digits=20,decimal_places=3, null=False, blank=False)
    loan_type                   = models.CharField(max_length=25)#[Small Loan, Small Business Loan],
    loan_application_date       = models.DateField()
    loan_disbursement_date      = models.DateField()
    first_repayment_date        = models.DateField(blank=True, null=True) #//optional in some cases
    loan_cycle_frequency        = models.CharField(max_length=10) #//must be of [Weekly, Monthly]
    loan_duration               = models.IntegerField(),
    loan_insurance_fee          = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True),
    loan_processing_fee         = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True) #// must be of length [9]
    loan_purpose                = models.CharField(max_length=25)
    loan_cycle                  = models.CharField(max_length=200, null=True, blank=True)
    loan_completed              = models.BooleanField(default=False)
    loan_completed_date         = models.DateTimeField(balnk=True, null=True)
    timestamp                   = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} Loan belongs to {} member".format(self.principal_amount, self.loan_applicant)
