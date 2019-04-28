from rest_framework import generics
from django.db.utils import IntegrityError 

from .models import Institution, InstitutionSettings, InstitutionStaff
from .serializers import InstitutionCreateSerializer, InstitutionSettingsCreateSerializer, InstitutionStaffCreateSerializer
from accounts.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from accounts.models import User
from helpers.helpers import get_object

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework import permissions
from accounts.permissions import BranchManagerPermissions, LoanClientPermissions, LoanOfficerPermissions, InstitutionAdministratorPermissions, InstitutionAdministratorAndLoanOfficerPermissions


class InstitutionList(APIView):
    """
    List all institutions and create institutions
    """
    permission_classes = (permissions.IsAuthenticated, InstitutionAdministratorPermissions)

    def post(self, request, format=None):
        serializer = InstitutionCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(created_by=self.request.user, is_institution_active=True)
                data_dict = {"status":201, "data":serializer.data}
                return Response(data_dict, status=status.HTTP_201_CREATED)
            except:
                return Response({'Error':'User has already created an institution'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InstitutionDetail(APIView):
    """
    Get institution Details
    """
    permission_classes = (permissions.IsAuthenticated, InstitutionAdministratorAndLoanOfficerPermissions)

    def get(self, request, pk, format=None):
        institution = get_object(Institution, pk)
        if institution:
            institution_serializer = InstitutionCreateSerializer(institution)
            return Response(institution_serializer.data, status=status.HTTP_200_OK)
        else:
            error_message_dict = {"status":404, "error":"Institution doesnot exist"}
            return Response(error_message_dict, status=status.HTTP_404_NOT_FOUND)

    # def put(self, request, pk, format=None):
    #     loan_group = get_object(Loans, pk)
    #     serializer = LoansSerializer(loan_group, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstitutionSettingsList(APIView):
    """
    List all insttitution settings and create an institution setting
    """
    permission_classes = (permissions.IsAuthenticated, InstitutionAdministratorPermissions)

    # def get(self, request, format=None):
    #     snippets = InstitutionSettings.objects.all()
    #     serializer = InstitutionSettingsCreateSerializer(snippets, many=True)
    #     data_dict = {"status":200, "data":serializer.data}
    #     return Response(data_dict, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = InstitutionSettingsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data_dict = {"status":201, "data":serializer.data}
            return Response(data_dict, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InstitutionSettingsDetail(APIView):
    """
    Get institution Settings Details
    """
    permission_classes = (permissions.IsAuthenticated, InstitutionAdministratorAndLoanOfficerPermissions)

    def get(self, request, pk, format=None):
        institution_settings = get_object(InstitutionSettings, pk)
        if institution_settings:
            institution_settings_serializer = InstitutionSettingsCreateSerializer(institution_settings)
            return Response(institution_settings_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("Institution doesnot exist", status=status.HTTP_404_NOT_FOUND)
