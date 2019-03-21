from django.contrib import admin
from .models import LoanGroup, GroupMember

admin.site.register(LoanGroup)
admin.site.register(GroupMember)
