from rest_framework import generics
from .models import LoanGroup
from .serializers import LoanGroupSerializer

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

class LoanGroupRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = LoanGroupSerializer

    def get_queryset(self):
        return LoanGroup.objects.all()

    def validate_group_name(self, value):
        qs=LoanGroup.objects.filter(group_name__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("Group Names must be unique")
        return value
