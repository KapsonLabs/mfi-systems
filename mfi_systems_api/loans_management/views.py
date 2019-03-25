from rest_framework import generics
from members.models import GroupMember
from .models import Loans
from .serializers import LoansSerializer, LoanStatusSerializer
from django.http import Http404
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework import permissions

from helpers.helpers import get_object

from accounts.permissions import BranchManagerPermissions, LoanClientPermissions, LoanOfficerPermissions

class LoansList(APIView):
    """
    List all groups and create a group.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        snippets = Loans.objects.all()
        serializer = LoansSerializer(snippets, many=True)
        related_links = 'links'
        data_dict = {"status":200, "links":related_links, "data":serializer.data}
        return Response(data_dict, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # request.data['responsible_loan_officer']=request.user
        loan = LoansSerializer(data=request.data)
        if loan.is_valid():
            loan.save(responsible_loan_officer=self.request.user)
            data_dict = {"status":201, "data":loan.data}
            return Response(data_dict, status=status.HTTP_201_CREATED)
        return Response(loan.errors, status=status.HTTP_400_BAD_REQUEST)

class LoansDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, pk, format=None):
        loan_group = get_object(Loans, pk)
        serializer = LoansSerializer(loan_group)
        data_with_link = dict(serializer.data)#["member"] = 'groups/{}/members/'.format(pk)
        links = {'members': 'api/v1/groups/{}/members/'.format(pk)}
        data_with_link['links'] = links
        data_dict = {"data":data_with_link, "status":200}
        return Response(data_dict, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        loan_group = get_object(Loans, pk)
        serializer = LoansSerializer(loan_group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        loan_group = get_object(Loans, pk)
        loan_group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LoansStatus(APIView):
    """
    Check and update loan status
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, pk, format=None):
        loan = get_object(Loans, pk)
        serializer = LoanStatusSerializer(loan)
        data_with_link = dict(serializer.data)#["member"] = 'groups/{}/members/'.format(pk)
        data_dict = {"data":data_with_link, "status":200}
        return Response(data_dict, status=status.HTTP_200_OK)