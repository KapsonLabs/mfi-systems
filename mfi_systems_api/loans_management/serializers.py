from rest_framework import serializers
from .models import Loans, LoanCycles, LoanApproval, LoanDisbursal, LoanPayments
from members.serializers import GroupMemberSerializer, ShortGroupMemberSerializer, ShortMemberSerializer
from accounts.serializers import UserSerializer

class LoansCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loans
        fields = ('id' ,'principal_amount', 'interest_rate', 'loan_type', 'loan_insurance_fee', 'loan_processing_fee', 'loan_cycle_frequency', 'loan_balance_to_pay', 'expected_duration' ,'loan_purpose', 'guarantor1', 'guarantor2', 'expected_income_corebznss', 'expected_profit_corebznss', 'corebznss_comment', 'loan_completed', 'loan_status', 'is_loan_disbursed', 'timestamp', 'responsible_loan_officer', 'loan_applicant')

class LoansSerializer(serializers.ModelSerializer):
    responsible_loan_officer = UserSerializer(read_only=True)
    loan_applicant = ShortGroupMemberSerializer(read_only=True)

    class Meta:
        model = Loans
        fields = ('id' ,'principal_amount', 'interest_rate', 'loan_type', 'loan_insurance_fee', 'loan_processing_fee', 'loan_cycle_frequency', 'loan_balance_to_pay', 'expected_duration' ,'loan_purpose', 'guarantor1', 'guarantor2', 'expected_income_corebznss', 'expected_profit_corebznss', 'corebznss_comment', 'loan_completed', 'loan_status', 'is_loan_disbursed', 'timestamp', 'responsible_loan_officer', 'loan_applicant')
        

    def create(self, validated_data):
        loan = super(LoansSerializer, self).create(validated_data)
        loan.interest_rate=0.1
        loan.loan_insurance_fee=(float(validated_data['principal_amount'])*0.01)
        loan.loan_processing_fee=(float(validated_data['principal_amount'])*0.01)
        loan.loan_balance_to_pay=(float(validated_data['principal_amount'])*0.1)+(float(validated_data['principal_amount']))
        loan.save()
        return loan

class ShortLoanSerializer(serializers.ModelSerializer):
    loan_applicant = ShortMemberSerializer(read_only=True)

    class Meta:
        model = Loans
        fields = ('id' ,'principal_amount', 'loan_balance_to_pay', 'loan_completed', 'timestamp', 'loan_applicant')


class LoanStatusSerializer(serializers.ModelSerializer):
    loan_applicant = GroupMemberSerializer(read_only=True)

    class Meta:
        model = Loans
        fields = ('loan_applicant', 'principal_amount', 'loan_insurance_fee', 'loan_processing_fee', 'next_payment_date', 'loan_cycle_frequency', 'loan_balance_to_pay', 'expected_duration', 'loan_completed', 'loan_status', 'is_loan_disbursed', 'timestamp')

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
        fields=('id', 'related_loan', 'cycle_date', 'amount_expected', 'loan_balance')

class LoanApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model=LoanApproval
        fields=('id', 'approved_by', 'loan_approved', 'date_approved')

class LoanDisbursalSerializer(serializers.ModelSerializer):
    class Meta:
        model=LoanDisbursal
        fields=('id', 'disbursed_by', 'disbursed_loan', 'date_disbursed')

class LoanPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=LoanPayments
        fields=('id', 'amount_paid', 'fined_amount', 'comment', 'transaction_status' ,'date_paid')
        read_only_fields = ('related_loan_cycle', )

class LoanCycleListSerializer(serializers.ModelSerializer):

    related_loan = ShortLoanSerializer(read_only=True)

    class Meta:
        model=LoanCycles
        fields=('id', 'cycle_date', 'amount_expected', 'amount_paid', 'balance', 'cycle_status', 'loan_balance', 'related_loan')

class LoanCycleUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model=LoanCycles
        fields=('id', 'related_loan', 'amount_paid', 'balance', 'cycle_status', 'loan_balance', 'cycle_date', 'amount_expected')
        # read_only_fields = ('amount_expected', )