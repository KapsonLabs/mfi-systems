from django.db import models
from accounts.models import User
from institution.models import Institution

class LoanGroup(models.Model):
    """
    Loan Group model
    """
    institution_id  = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='institution_group', default=1)
    group_name      = models.CharField(max_length=15)
    date_created    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} Group".format(self.group_name)

class GroupMember(models.Model):
    """
    Group Member Model
    """
    group_id                    = models.ForeignKey(LoanGroup, on_delete=models.CASCADE, related_name='member_group')
    user_id                     = models.OneToOneField(User, on_delete=models.CASCADE, related_name='related_member_user')
    date_of_birth               = models.DateField()
    shares_held                 = models.IntegerField(blank=True, null=True)
    member_active               = models.BooleanField(default=False)
    gender                      = models.CharField(max_length=8)
    membership_fee              = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    shares_fee                  = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    employment                  = models.CharField(max_length=30)
    phone_dialing_code          = models.CharField(max_length=4)
    phone_number                = models.CharField(max_length=12) #must be of length [9]
    marital_status              = models.CharField(max_length=15) #must be of [single, deserted, divorced, widow/widower, married]
    spouse_full_name            = models.CharField(max_length=25, blank=True, null=True) #optional if not married
    id_number                   = models.CharField(max_length=30)
    id_attachment_front         = models.ImageField(upload_to='images/', blank=True, null=True)#[image_front_face, image_back_face],
    id_attachment_back          = models.ImageField(upload_to='images/', blank=True, null=True)#[image_front_face, image_back_face],
    profile_picture             = models.ImageField(upload_to='images/', blank=True, null=True)
    utility_bill                = models.FileField(upload_to='documents/', blank=True, null=True)
    present_village             = models.CharField(max_length=20)
    present_subcounty           = models.CharField(max_length=20)
    present_county              = models.CharField(max_length=20)
    present_division            = models.CharField(max_length=20)
    present_district            = models.CharField(max_length=20)
    date_created                = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} Member belongs to {} group".format(self.user_id.username, self.group_id)

class SavingsAccount(models.Model):
    """
    Savings Account
    """
    group_member_related        = models.ForeignKey(GroupMember, on_delete=models.CASCADE, related_name="savings_account_owner")
    account_number              = models.CharField(max_length=20)
    account_balance             = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    running_balance             = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    interest_accrued            = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    date_created                = models.DateTimeField(auto_now_add=True)

class SharesAccount(models.Model):
    """
    Shares Account
    """
    group_member_related        = models.ForeignKey(GroupMember, on_delete=models.CASCADE, related_name="shares_account_owner")
    account_number              = models.CharField(max_length=20)
    shares_owned                = models.IntegerField(default=0)
    account_balance             = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    running_balance             = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    interest_accrued            = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    date_created                = models.DateTimeField(auto_now_add=True)

class SavingsPayments(models.Model):
    """
    Savings Payments Model
    """
    savings_account_related     = models.ForeignKey(SavingsAccount, on_delete=models.CASCADE, related_name="savings_account_related")
    transaction_number          = models.CharField(max_length=100, null=True, blank=True)
    amount_paid                 = models.DecimalField(max_digits=20, decimal_places=3)
    date_paid                   = models.DateTimeField(auto_now_add=True)

class SharesPayments(models.Model):
    """
    Shares Payments Model
    """
    shares_account_related      = models.ForeignKey(SharesAccount, on_delete=models.CASCADE, related_name="savings_account_related")
    transaction_number          = models.CharField(max_length=100, null=True, blank=True)
    amount_paid                 = models.DecimalField(max_digits=20, decimal_places=3)
    shares_bought               = models.IntegerField(null=True, blank=True)
    date_paid                   = models.DateTimeField(auto_now_add=True)

class SavingsWithdrawal(models.Model):
    """
    Savings Withdrawal Model
    """
    savings_account_related     = models.ForeignKey(SavingsAccount, on_delete=models.CASCADE, related_name="savings_account_withdrawal")
    transaction_number          = models.CharField(max_length=100, null=True, blank=True)
    amount_withdrawn            = models.DecimalField(max_digits=20, decimal_places=3)
    date_withdrawn              = models.DateTimeField(auto_now_add=True)


