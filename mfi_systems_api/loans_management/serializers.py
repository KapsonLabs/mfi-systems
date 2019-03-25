from rest_framework import serializers
from .models import Loans, LoanCycles, LoanApproval, LoanDisbursal

class LoansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loans
        fields = ('id', 'loan_applicant', 'principal_amount', 'interest_rate', 'loan_type', 'loan_insurance_fee', 'loan_processing_fee', 'loan_cycle_frequency', 'loan_balance_to_pay', 'expected_duration' ,'loan_purpose', 'guarantor1', 'guarantor2', 'expected_income_corebznss', 'expected_profit_corebznss', 'corebznss_comment', 'loan_completed', 'loan_status', 'is_loan_disbursed', 'timestamp')

    def create(self, validated_data):
        loan = super(LoansSerializer, self).create(validated_data)
        loan.interest_rate=0.1
        loan.loan_insurance_fee=(float(validated_data['principal_amount'])*0.01)
        loan.loan_processing_fee=(float(validated_data['principal_amount'])*0.01)
        loan.loan_balance_to_pay=(float(validated_data['principal_amount'])*0.1)+(float(validated_data['principal_amount']))
        loan.save()
        return loan

class LoanStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loans
        fields = ('loan_applicant', 'principal_amount', 'interest_rate', 'loan_type', 'loan_insurance_fee', 'loan_processing_fee', 'loan_cycle_frequency', 'loan_balance_to_pay', 'expected_duration', 'loan_completed', 'loan_status', 'is_loan_disbursed', 'timestamp')

class UpdateLoanStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Loans
        fields=('id','loan_status', )


class DisburseLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model=Loans
        fields=('id','is_loan_disbursed', 'next_payment_date')

class LoanCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model=LoanCycles
        fields=('id', 'loan', 'cycle_date', 'amount_expected')

class LoanApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model=LoanApproval
        fields=('id', 'approved_by', 'loan_approved', 'date_approved')

class LoanDisbursalSerializer(serializers.ModelSerializer):
    class Meta:
        model=LoanDisbursal
        fields=('id', 'disbursed_by', 'disbursed_loan', 'date_disbursed')