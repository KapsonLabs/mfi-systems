from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ('id', 'loan_applicant', 'principal_amount', 'loan_type', 'loan_cycle_frequency', 'expected_duration' ,'loan_purpose', 'guarantor1', 'guarantor2', 'expected_income_corebznss', 'expected_profit_corebznss', 'corebznss_comment')

    def create(self, validated_data):
        loan = super(LoanSerializer, self).create(validated_data)
        # loan.interest_rate=1
        # loan.loan_insurance_fee=(float(validated_data['principal_amount'])*0.01)
        # loan.responsible_loan_officer=2
        loan.save()
        return loan