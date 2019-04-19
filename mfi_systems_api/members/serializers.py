from members.models import LoanGroup, GroupMember, SavingsAccount, SharesAccount
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
        fields = ('id', 'user_id' ,'group_id', 'date_of_birth', 'gender', 'membership_fee', 'shares_fee', 'employment', 'phone_dialing_code', 'phone_number', 'marital_status', 'spouse_full_name', 'id_number', 'id_attachment_front', 'id_attachment_back', 'profile_picture', 'present_village', 'present_subcounty', 'present_county', 'present_division', 'present_district', 'date_created')

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