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
        fields = ('id', 'user_id','group_id', 'date_of_birth','gender', 'employment', 'phone_dialing_code','phone_number', 'marital_status', 'spouse_full_name', 'id_number','id_attachment_front', 'id_attachment_back', 'profile_picture', 'present_village', 'present_subcounty', 'present_county', 'present_division', 'present_district', 'date_created')


    # def create(self, validated_data):
    #     """
    #     Overriding the default create method of the Model serializer.
    #     :param validated_data: data containing all the details of student
    #     :return: returns a successfully created student record
    #     """
    #     user_data = validated_data.pop('user')
    #     user = UserSerializer.create(UserSerializer(), validated_data=user_data)
    #     member, created = GroupMember.objects.update_or_create(user=user,
    #                         subject_major=validated_data.pop('subject_major'))
    #     return member