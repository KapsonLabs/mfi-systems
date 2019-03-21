from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ('loan_applicant', 'username', 'first_name' ,'other_names', 'email_address', 'date_of_birth','gender', 'employment', 'phone_dialing_code','phone_number', 'marital_status', 'spouse_full_name', 'id_number','id_attachment_front', 'id_attachment_back', 'profile_picture', 'present_village', 'present_subcounty', 'present_county', 'present_division', 'present_district')