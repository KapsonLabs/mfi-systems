from members.models import LoanGroup, GroupMember
from accounts.serializers import UserSerializer
from accounts.models import User
from rest_framework import serializers

class LoanGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanGroup
        fields = ('id', 'group_name', 'branch_name', 'date_created')

class GroupMemberSerializer(serializers.ModelSerializer):
    """
    A group member serializer to return the member details
    """

    class Meta:
        model = GroupMember
        fields = ('id', 'user_id' ,'group_id', 'date_of_birth','gender', 'employment', 'phone_dialing_code','phone_number', 'marital_status', 'spouse_full_name', 'id_number','id_attachment_front', 'id_attachment_back', 'profile_picture', 'present_village', 'present_subcounty', 'present_county', 'present_division', 'present_district', 'date_created')


class GroupMemberListSerializer(serializers.ModelSerializer):
    """
    A group member serializer to return the member details
    """
    user_id = UserSerializer(read_only=True)
    class Meta:
        model = GroupMember
        fields = ('id', 'user_id' ,'group_id', 'date_of_birth','gender', 'employment', 'phone_dialing_code','phone_number', 'marital_status', 'spouse_full_name', 'id_number','id_attachment_front', 'id_attachment_back', 'profile_picture', 'present_village', 'present_subcounty', 'present_county', 'present_division', 'present_district', 'date_created')


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