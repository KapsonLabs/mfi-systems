from django.db import models
from members.models import GroupMember

class SavingsAccounts(models.Model):
    """
    Savings Account Model
    """ 
    account_holder      = models.ForeignKey(GroupMember, on_delete=models.CASCADE, related_name='savings_account')
    amount_number       = models.CharField(max_digits=100, blank=False, null=False)
    savings_type        = models.CharField(max_digits=100, blank=False, null=False) 
    date_created        = models.DateTimeField(auto_now_add=True)

class AccountBalances(models.Model):
    """
    Account Balances Model
    """ 
    related_account     = models.ForeignKey(SavingsAccounts, on_delete=models.CASCADE, related_name='related_account')
    running_balance     = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    interest_accrued    = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    timestamp           = models.DateTimeField(auto_now_add=True)

class AccountTransactions(models.Model):
    """
    Account Transactions Model
    """
    transaction_account     = models.ForeignKey(SavingsAccounts, on_delete=models.CASCADE, related_name='transaction_account') 
    transaction_type        = models.CharField(max_digits=100, blank=False, null=False) 
    transaction_amount      = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    transaction_status      = models.BooleanField(default=False)
    txn_status_comment      = models.TextField()
    transaction_timestamp   = models.DateTimeField(auto_now_add=True)