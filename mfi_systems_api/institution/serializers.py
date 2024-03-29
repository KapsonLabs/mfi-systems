from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Institution, InstitutionSettings, InstitutionStaff

class InstitutionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institution
        fields = ('id','institution_name', 'institution_type', 'location', 'certificate_of_incoporation', 'date_of_incoporation', 'date_created')

class InstitutionSettingsCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstitutionSettings
        fields = ('id', 'institution_id', 'membership_fee', 'membership_fee_frequency', 'share_price', 'minimum_shares', 'maximum_shares','savings_amount', 'savings_frequency', 'savings_interest', 'savings_interest_calculator', 'maximum_savings_to_withdraw','maximum_monthly_withdraws','savings_interest_frequency','loan_types_provided', 'quick_loan_interest_rate', 'small_loan_interest_rate', 'big_loan_interest_rate', 'quick_loan_limit','quick_loan_repayment_limit', 'percentage_of_savings_rq_loan', 'loan_interest_rate', 'small_loan_interest_calculator','quick_loan_interest_calculator', 'big_loan_interest_calculator', 'loan_guarantors_required', 'loan_processing_fee_percentage','loan_insurance_fee_percentage', 'date_created')

class InstitutionStaffCreateSerializer(serializers.ModelSerializer):

    user_id = UserSerializer(read_only=True)

    class Meta:
        model = InstitutionStaff
        fields = ('id', 'user_id', 'institution_id', 'staff_role', 'staff_responsibility', 'phone_dialing_code','phone_number','date_created')