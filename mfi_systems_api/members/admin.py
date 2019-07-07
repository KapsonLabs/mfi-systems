from django.contrib import admin
from .models import LoanGroup, GroupMember, SavingsAccount, SharesAccount

admin.site.register(LoanGroup)
admin.site.register(GroupMember)
admin.site.register(SavingsAccount)
