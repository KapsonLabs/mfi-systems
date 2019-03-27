from rest_framework import generics
from members.models import LoanGroup, GroupMember
from rest_framework.views import APIView
from rest_framework import permissions
from loans_management.models import Loans
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Avg, Count, Min, Sum

class StatisticsView(APIView):
    """
    Statistics for mfi
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        registered_members = GroupMember.objects.all().count()
        total_principal = Loans.objects.all().aggregate(principal_amount = Sum('principal_amount'))
        total_interest_expected =  Loans.objects.all().aggregate(loan_balance_to_pay = Sum('loan_balance_to_pay'))
        total_outstanding_open_loans = Loans.objects.all().filter(loan_status=False).count()
        total_open_loans =  Loans.objects.all().filter(loan_status=False).count()
        fully_paid_loans = Loans.objects.all().filter(loan_completed=True).count()
        unpaid_loans = Loans.objects.all().filter(loan_completed=False).count()
        undisbursed_loans = Loans.objects.all().filter(is_loan_disbursed=False).count()
        statistics={
            "registered_members":registered_members,
            "total_principal":total_principal['principal_amount'],
            "total_interest_expected":total_interest_expected['loan_balance_to_pay'],
            "total_outstanding_open_loans":total_outstanding_open_loans,
            "total_open_loans":total_open_loans,
            "fully_paid_loans":fully_paid_loans,
            "unpaid_loans":unpaid_loans,
            "undisbursed_loans":undisbursed_loans,
        }
        data_dict = {"status":200, "data":statistics}
        return Response(data_dict, status=status.HTTP_200_OK)