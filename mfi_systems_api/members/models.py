from django.db import models

class LoanGroup(models.Model):
    group_name   = models.CharField(max_length=15)
    branch_name  = models.CharField(max_length=15)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} Group belongs to {} branch".format(self.group_name, self.branch_name)