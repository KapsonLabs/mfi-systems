from members.models import LoanGroup
from rest_framework import serializers

class LoanGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanGroup
        fields = ('group_name', 'branch_name')