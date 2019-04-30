import uuid

from members.models import LoanGroup, GroupMember, SavingsAccount, SharesAccount, SavingsPayments, SharesPayments, SavingsWithdrawal
from accounts.serializers import UserSerializer
from accounts.models import User
from institution.models import InstitutionSettings, Institution
from rest_framework import serializers

from helpers.helpers import get_object

class LoanGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanGroup
        fields = ('id', 'institution_id' , 'group_name', 'date_created')


class GroupMemberSerializer(serializers.ModelSerializer):
    """
    A group member serializer to return the member details
    """

    class Meta:
        model = GroupMember
        fields = ('id' ,'group_id', 'date_of_birth', 'gender', 'membership_fee', 'shares_fee', 'employment', 'phone_dialing_code', 'phone_number', 'marital_status', 'spouse_full_name', 'id_number', 'id_attachment_front', 'id_attachment_back', 'profile_picture', 'present_village', 'present_subcounty', 'present_county', 'present_division', 'present_district', 'date_created')

    def validate_membership_fee(self, value):
        """
        Check that the membership fee being paid is equal or more than the group membership fee 
        """
        group = get_object(LoanGroup, self.initial_data['group_id'])
        institution_settings = get_object(InstitutionSettings, group.institution_id.pk)
        if value < institution_settings.membership_fee:
            raise serializers.ValidationError("Membership fee not sufficient to join group")
        return value

    def validate_shares_fee(self, value):
        """
        Check that the shares_fee being paid is sufficient to cover the minimum share fee required
        """
        group = get_object(LoanGroup, self.initial_data['group_id'])
        institution_settings = get_object(InstitutionSettings, group.institution_id.pk)
        if value < institution_settings.share_price:
            raise serializers.ValidationError("Shares fee not sufficient to cover minimum share amount")
        return value

    def validate_phone_number(self, value):
        """
        Check that the phone number conforms to the agreed standard
        """
        if len(value) != 9:
            raise serializers.ValidationError("Phone number doesnt conform to the standard")
        return value


class GroupMemberListSerializer(serializers.ModelSerializer):
    """
    A group member serializer to return the member details
    """
    user_id = UserSerializer(read_only=True)
    class Meta:
        model = GroupMember
        fields = ('id', 'user_id' ,'group_id', 'date_of_birth','gender', 'employment', 'phone_dialing_code','phone_number', 'marital_status', 'spouse_full_name', 'id_number','id_attachment_front', 'id_attachment_back', 'profile_picture', 'present_village', 'present_subcounty', 'present_county', 'present_division', 'present_district', 'date_created')


class MemberPaymentsSerializer(serializers.ModelSerializer):
    """
    A serialiser that returns the necessary paynents for registration.
    """
    class Meta:
        model = InstitutionSettings
        fields = ('membership_fee', 'share_price')

class MemberSavingsPaymentsSerializer(serializers.ModelSerializer):
    """
    A serializer that returns the savings payments to be made.
    """
    class Meta:
        model = InstitutionSettings
        fields = ("savings_amount",)


class ShortGroupMemberSerializer(serializers.ModelSerializer):
    """
    A group member serializer to return the member details
    """
    user_id = UserSerializer(read_only=True)
    group_id = LoanGroupSerializer(read_only=True)

    class Meta:
        model = GroupMember
        fields = ('id', 'user_id' ,'group_id', 'date_of_birth','gender', 'employment', 'phone_dialing_code','phone_number')

class ShortMemberSerializer(serializers.ModelSerializer):
    """
    A short member serializer to return the some member details
    """
    user_id = UserSerializer(read_only=True)

    class Meta:
        model = GroupMember
        fields = ('id', 'user_id', 'phone_dialing_code','phone_number')


class SavingsAccountSerializer(serializers.ModelSerializer):
    """
    A savings account serializer
    """

    class Meta:
        model = SavingsAccount
        fields = ('id', 'group_member_related', 'account_number', 'account_balance', 'running_balance', 'interest_accrued')


class SharesAccountSerializer(serializers.ModelSerializer):
    """
    A shares account serializer
    """
    
    class Meta:
        model = SharesAccount
        fields = ('id', 'group_member_related', 'account_number', 'account_balance', 'running_balance', 'interest_accrued')

class SavingsPaymentsSerializer(serializers.ModelSerializer):
    """
    A savings payment's serializer 
    """

    class Meta:
        model = SavingsPayments
        fields = ('id', 'savings_account_related', 'transaction_number', 'amount_paid', 'date_paid')
        read_only_fields = ('date_paid', )
        
    def validate_amount_paid(self, value):
        savings_account = get_object(SavingsAccount, self.initial_data['savings_account_related'])
        group = get_object(LoanGroup, savings_account.group_member_related.group_id.pk)
        institution_settings = get_object(InstitutionSettings, group.institution_id.pk)
        if value < institution_settings.savings_amount:
            raise serializers.ValidationError("Saving fee not sufficient for the cycle")
        return value

    def create(self, validated_data):
        savings_payment = super(SavingsPaymentsSerializer, self).create(validated_data)
        savings_payment.transaction_number = uuid.uuid4()
        savings_payment.save()
        return savings_payment


class SharesPaymentsSerializer(serializers.ModelSerializer):
    """
    A shares payment's serializer
    """

    class Meta:
        model = SharesPayments
        fields = ('id', 'shares_account_related', 'transaction_number', 'amount_paid', 'shares_bought')

class SavingsWithdrawalSerializer(serializers.ModelSerializer):
    """
    A savings withdrawal serializer
    """

    class Meta:
        model = SavingsWithdrawal
        fields = ("amount_withdrawn", )

    def validate_amount_withdrawn(self, value):
        savings_account_related = SavingsAccount.objects.get(account_number=self.initial_data['account_number'])
        if value > savings_account_related.account_balance:
            raise serializers.ValidationError("Your account balance is insufficient to make the withdraw")
        return value

    def create(self, validated_data):
        savings_withdrawal = super(SavingsWithdrawalSerializer, self).create(validated_data)
        savings_withdrawal.transaction_number = uuid.uuid4()
        savings_withdrawal.save()
        return savings_withdrawal

class AccountNumberSerializer(serializers.Serializer):
    """
    An account number serializer for checking statuses
    """
    account_number = serializers.CharField(max_length=20)

    def validate_amount_number(self, value):
        if len(value) != 16:
           raise serializers.ValidationError("Invalid/wrong account number entered")
        return value 