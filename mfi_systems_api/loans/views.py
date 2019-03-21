from rest_framework import generics
from members.models import LoanGroup, GroupMember
from django.http import Http404
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

class GroupList(APIView):
    """
    List all groups and create a group.
    """
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