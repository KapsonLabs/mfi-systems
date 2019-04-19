from rest_framework import generics
from .models import Institution, InstitutionSettings, InstitutionStaff
from .serializers import InstitutionCreateSerializer, InstitutionSettingsCreateSerializer, InstitutionStaffCreateSerializer
from accounts.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from accounts.models import User

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework import permissions
from accounts.permissions import BranchManagerPermissions, LoanClientPermissions, LoanOfficerPermissions


class InstitutionList(APIView):
    """
    List all institutions and create institutions
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        snippets = Institution.objects.all()
        serializer = InstitutionCreateSerializer(snippets, many=True)
        data_dict = {"status":200, "data":serializer.data}
        return Response(data_dict, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = InstitutionCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            data_dict = {"status":201, "data":serializer.data}
            return Response(data_dict, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstitutionSettingsList(APIView):
    """
    List all insttitution settings and create an institution setting
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        snippets = InstitutionSettings.objects.all()
        serializer = InstitutionSettingsCreateSerializer(snippets, many=True)
        data_dict = {"status":200, "data":serializer.data}
        return Response(data_dict, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = InstitutionSettingsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data_dict = {"status":201, "data":serializer.data}
            return Response(data_dict, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
