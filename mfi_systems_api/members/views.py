from rest_framework import generics
from .models import LoanGroup, GroupMember, SavingsAccount, SharesAccount
from institution.models import InstitutionSettings
from .serializers import LoanGroupSerializer, GroupMemberSerializer, GroupMemberListSerializer, MemberPaymentsSerializer, SavingsAccountSerializer, SharesAccountSerializer
from accounts.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from accounts.models import User

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework import permissions
from helpers.helpers import get_object, generate_account_number, send_sms
from accounts.permissions import BranchManagerPermissions, LoanClientPermissions, LoanOfficerPermissions

class GroupList(APIView):
    """
    List all groups and create a group.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        snippets = LoanGroup.objects.all()
        serializer = LoanGroupSerializer(snippets, many=True)
        related_links = 'links'
        data_dict = {"status":200, "links":related_links, "data":serializer.data}
        return Response(data_dict, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = LoanGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data_dict = {"status":201, "data":serializer.data}
            return Response(data_dict, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, pk):
        try:
            return LoanGroup.objects.get(pk=pk)
        except LoanGroup.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        loan_group = self.get_object(pk)
        serializer = LoanGroupSerializer(loan_group)
        data_with_link = dict(serializer.data)#["member"] = 'groups/{}/members/'.format(pk)
        links = {'members': 'api/v1/groups/{}/members/'.format(pk)}
        data_with_link['links'] = links
        data_dict = {"data":data_with_link, "status":200}
        return Response(data_dict, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        loan_group = self.get_object(pk)
        serializer = LoanGroupSerializer(loan_group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        loan_group = self.get_object(pk)
        loan_group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserClientCreate(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        data_dict = {"status":200, "data":serializer.data}
        return Response(data_dict, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user_client_serializer = UserSerializer(data=request.data)
        #print(serializer)
        if user_client_serializer.is_valid():
            user_client_serializer.save()
            # user = user_client_serializer.create
            # print(user)
            data_dict = {"status":201, "data":user_client_serializer.data, 'id':user_client_serializer.data['id']}
            return Response(data_dict, status=status.HTTP_201_CREATED)
        return Response(user_client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user_detail = self.get_object(pk)
        serializer = UserSerializer(user_detail)
        # data_with_link = dict(serializer.data)#["member"] = 'groups/{}/members/'.format(pk)
        # links = {'members': 'api/v1/groups/{}/members/'.format(pk)}
        # data_with_link['links'] = links
        data_dict = {"data":serializer.data, "status":200}
        return Response(data_dict, status=status.HTTP_200_OK)    

class MemberFeesPayment(APIView):
    """
    Get the member fees to be paid on registration
    """
    permission_classes = (permissions.IsAuthenticated, LoanOfficerPermissions)

    def get(self, request, pk, format=None):
        group = get_object(LoanGroup, pk)
        institution_settings = get_object(InstitutionSettings, group.institution_id.pk)
        payment_serializer = MemberPaymentsSerializer(institution_settings)
        data_dict = {"fees_to_pay":payment_serializer.data, "status":200}
        return Response(data_dict, status=status.HTTP_200_OK)


class MemberList(APIView):
    """
    List all members and create a new member.
    """
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request, format=None):
        members = GroupMember.objects.all()
        serializer = GroupMemberListSerializer(members, many=True)
        data_dict = {"status":200, "data":serializer.data}
        return Response(data_dict, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        member_serializer = GroupMemberSerializer(data=request.data)
        if member_serializer.is_valid():
            member_serializer.save()
            #create savings and shares accounts
            savings_account_number = generate_account_number(member_serializer.data['id'], "savings")
            savings_account = {
                'group_member_related':member_serializer.data['id'],
                'account_number': savings_account_number
                # 'account_balance':0,
                # 'running_balance':0,
                # 'interest_accrued':0
            }
            savings_account_creation = SavingsAccountSerializer(data=savings_account)
            savings_account_creation.is_valid(raise_exception=True)
            savings_account_creation.save()
            
            #create shares account
            shares_account_number = generate_account_number(member_serializer.data['id'], 'shares')
            shares_account = {
                'group_member_related':member_serializer.data['id'],
                'account_number': shares_account_number
                # 'account_balance':0,
                # 'running_balance':0,
                # 'interest_accrued':0
            }
            shares_account_creation = SharesAccountSerializer(data=shares_account)
            shares_account_creation.is_valid(raise_exception=True)
            shares_account_creation.save()

            #send twilio sms with registration details
            phone_number = "{}{}".format(member_serializer.data['phone_dialing_code'], member_serializer.data['phone_number'])
            message = "Welcome to MFI, Your savings account Number is {} with a balance of {} shs and your shares account Number is {} with a balance of {} shs".format(savings_account_number, 0, shares_account_number, 0)
            try:
                send_sms(phone_number, message)
            except:
                print("Message Not sending")
            data_dict = {"status":201, "data":member_serializer.data, "savings_account":savings_account, "shares_account":shares_account}
            return Response(data_dict, status=status.HTTP_201_CREATED)
        return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberDetail(APIView):
    """
    Retrieve, update or delete a member instance
    """
    permission_classes = (permissions.IsAuthenticated, )
    def get_object(self, pk):
        try:
            return GroupMember.objects.get(pk=pk)
        except GroupMember.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        group_member = self.get_object(pk)
        serializer = GroupMemberListSerializer(group_member)
        data_with_link = dict(serializer.data)
        links = {'loans': 'api/v1/members/{}/loans/'.format(pk)}
        data_with_link['links'] = links
        data_dict = {"status":200, "data":data_with_link}
        return Response(data_dict, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        group_member = self.get_object(pk)
        serializer = GroupMemberListSerializer(group_member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        group_member = self.get_object(pk)
        group_member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GroupMemberList(APIView):
    """
    List all members that belong to a particular group
    """
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request, pk, format=None):
        group_members = GroupMember.objects.filter(group_id=pk)
        print(group_members)
        serializer = GroupMemberSerializer(group_members, many=True)
        data_dict = {"status":200, "data":serializer.data}
        return Response(data_dict, status=status.HTTP_200_OK)