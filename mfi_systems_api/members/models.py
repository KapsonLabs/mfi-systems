from django.db import models
from accounts.models import User

class LoanGroup(models.Model):
    """
    Loan Group model
    """
    group_name   = models.CharField(max_length=15)
    branch_name  = models.CharField(max_length=15)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} Group belongs to {} branch".format(self.group_name, self.branch_name)

class GroupMember(models.Model):
    """
    Group Member Model
    """
    group_id                    = models.ForeignKey(LoanGroup, on_delete=models.CASCADE, related_name='member_group')
    user_id                     = models.OneToOneField(User, on_delete=models.CASCADE, related_name='related_member_user')
    date_of_birth               = models.DateField()
    gender                      = models.CharField(max_length=8)
    employment                  = models.CharField(max_length=30)
    phone_dialing_code          = models.CharField(max_length=4)
    phone_number                = models.CharField(max_length=12) #must be of length [9]
    marital_status              = models.CharField(max_length=15) #must be of [single, deserted, divorced, widow/widower, married]
    spouse_full_name            = models.CharField(max_length=25, blank=True, null=True) #optional if not married
    id_number                   = models.CharField(max_length=30)
    id_attachment_front         = models.ImageField(upload_to='images', blank=True, null=True)#[image_front_face, image_back_face],
    id_attachment_back          = models.ImageField(upload_to='images', blank=True, null=True)#[image_front_face, image_back_face],
    profile_picture             = models.ImageField(upload_to='images', blank=True, null=True)
    present_village             = models.CharField(max_length=20)
    present_subcounty           = models.CharField(max_length=20)
    present_county              = models.CharField(max_length=20)
    present_division            = models.CharField(max_length=20)
    present_district            = models.CharField(max_length=20)
    date_created                = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} Member belongs to {} group".format(self.user_id.username, self.group_id)