from rest_framework import generics
from django.db.utils import IntegrityError 
from django.http import QueryDict

from .models import Institution, InstitutionSettings, InstitutionStaff
from .serializers import InstitutionCreateSerializer, InstitutionSettingsCreateSerializer, InstitutionStaffCreateSerializer
from accounts.serializers import UserSerializer, InstitutionUserSerializer
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

class InstitutionStaffCreate(APIView):

    permission_classes = (permissions.IsAuthenticated, InstitutionAdministratorPermissions)
    def post(self, request, format=None):
        staff_data = request.data.copy()
        # try:
        username    = staff_data.pop('username', None)
        first_name  = staff_data.pop('first_name', None)
        last_name   = staff_data.pop('last_name', None)
        email       = staff_data.pop('email', None)
        password    = staff_data.pop('password', None)

        user_data_dict = {
        'username':username[0],
        'first_name':first_name[0],
        'last_name': last_name[0],
        'email':email[0],
        'password':password[0],
        }

        #recreating the query dict
        user_data_query_dict = QueryDict('', mutable=True)
        user_data_query_dict.update(user_data_dict)

        staff_serializer = InstitutionStaffCreateSerializer(data=staff_data)
        if staff_serializer.is_valid():
            #add query dict to user serializer
            user_account_serializer = InstitutionUserSerializer(data=user_data_query_dict)
            user_account_serializer.is_valid(raise_exception=True)
            if staff_serializer.validated_data['staff_role'] == 'LOAN_OFFICER':
                user_account_serializer.save(is_loan_officer=True)
            else:
                user_account_serializer.save(is_branch_manager=True)

            user = User.objects.get(pk=user_account_serializer.data['id'])
        
            staff_serializer.save(user_id=user)
    
            #send twilio sms with registration details
            phone_number = "{}{}".format(staff_serializer.data['phone_dialing_code'], staff_serializer.data['phone_number'])
            message = "Welcome to MFI, Your one time password is 0098"
            try:
                send_sms(phone_number, message)
            except:
                print("Message Not sending")
            data_dict = {"status":201, "data":staff_serializer.data}
            return Response(data_dict, status=status.HTTP_201_CREATED)
            # except:
            #     print("Failed")
            #     # return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(staff_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

