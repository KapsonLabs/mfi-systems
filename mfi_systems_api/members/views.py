from rest_framework import generics
from .models import LoanGroup, GroupMember
from .serializers import LoanGroupSerializer, GroupMemberSerializer
from accounts.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework import permissions
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

class MemberList(APIView):
    """
    List all members and create a new member.
    """
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request, format=None):
        members = GroupMember.objects.all()
        serializer = GroupMemberSerializer(members, many=True)
        data_dict = {"status":200, "data":serializer.data}
        return Response(data_dict, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        member_serializer = GroupMemberSerializer(data=request.data)
        #print(serializer)
        if member_serializer.is_valid():
            member_serializer.save()
            data_dict = {"status":201, "data":member_serializer.data}
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
        serializer = GroupMemberSerializer(group_member)
        data_with_link = dict(serializer.data)
        links = {'loans': 'api/v1/members/{}/loans/'.format(pk)}
        data_with_link['links'] = links
        data_dict = {"status":200, "data":data_with_link}
        return Response(data_dict, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        group_member = self.get_object(pk)
        serializer = GroupMemberSerializer(group_member, data=request.data)
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