import datetime

from rest_framework import generics
from members.models import GroupMember
from .models import Loans, LoanCycles
from .serializers import LoansSerializer, LoanStatusSerializer, UpdateLoanStatusSerializer, DisburseLoanSerializer, LoanCycleSerializer, LoanApprovalSerializer, LoanDisbursalSerializer, LoanCycleListSerializer, LoanPaymentsSerializer, LoanCycleUpdateSerializer,ShortGroupMemberSerializer, LoansCreateSerializer
from django.http import Http404
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework import permissions

from helpers.helpers import get_object, calculate_next_payment_date, calculate_payment_cycles, calculate_balance

from accounts.permissions import BranchManagerPermissions, LoanClientPermissions, LoanOfficerPermissions

class LoansList(APIView):
    """
    List all groups and create a group.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        related_links = 'links'
        loan_status = self.request.query_params.get('status', None)
        loans = Loans.objects.all()

        if loan_status is not None:
            if loan_status=='unapproved':
                loans = loans.filter(loan_status=False)
            elif loan_status=='approved':
                loans = loans.filter(loan_status=True)
            elif loan_status=='disbursed':
                loans = loans.filter(is_loan_disbursed=True)
            elif loan_status=='completed':
                loans = loans.filter(loan_completed=True)
        else:
            pass

        serializer = LoansSerializer(loans, many=True)
        data_dict = {"status":200, "links":related_links, "data":serializer.data,}
        return Response(data_dict, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # request.data['responsible_loan_officer']=request.user
        loan = LoansCreateSerializer(data=request.data)
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
        data_with_link = dict(serializer.data)
        data_dict = {"data":data_with_link, "status":200}
        return Response(data_dict, status=status.HTTP_200_OK)

class LoanStatusUpdate(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, pk ,*args, **kwargs):
        instance = get_object(Loans, pk)
        if request.data['loan_status'] == 'Approve' and instance.loan_status==False:
            loan_status={'loan_status':True}
            serializer = UpdateLoanStatusSerializer(
                instance=instance,
                data=loan_status
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # loan approval part auditing
            # loan_approved={'loan_approved':pk, }
            # loan_approver=LoanApprovalSerializer(
            #     data=loan_approved,
            # )
            
            # loan_approver.is_valid(raise_exception=True)
            # loan_approver.save(approved_by=request.user)

            loan_status_dict={"data":serializer.data, "status":200, "message":"Loan approved successfully, You can now disburse it"}
        elif request.data['loan_status'] == 'Disapprove' and instance.loan_status==True:
            loan_status={'loan_status':False}
            serializer = UpdateLoanStatusSerializer(
                instance=instance,
                data=loan_status
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # loan approval part auditing
            # loan_approved={'loan_approved':pk, }
            # loan_approver=LoanApprovalSerializer(
            #     data=loan_approved,
            # )
            
            # loan_approver.is_valid(raise_exception=True)
            # loan_approver.save(approved_by=request.user)

            loan_status_dict={"data":serializer.data, "status":200, "message":"Loan disapproved successfully"}
        else:
            loan_status_dict={"status":200, "error":"Loan has already been approved"}
        return Response(loan_status_dict, status=status.HTTP_200_OK)


class LoanDisbursement(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, pk ,*args, **kwargs):
        instance = get_object(Loans, pk)
        if request.data['is_loan_disbursed'] == 'Disburse' and instance.loan_status==True and instance.is_loan_disbursed==False:
            next_payment_date = calculate_next_payment_date(instance.loan_cycle_frequency, datetime.datetime.now())
            loan_disburse={'is_loan_disbursed':True, 'next_payment_date':next_payment_date}
            serializer = DisburseLoanSerializer(
                instance=instance,
                data=loan_disburse
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            try:
                cycles = calculate_payment_cycles(int(instance.expected_duration), instance.loan_cycle_frequency, float(instance.loan_balance_to_pay), instance.next_payment_date)
                for cycle in cycles:
                    cycle['related_loan'] = pk
                    cycle['loan_balance'] = instance.loan_balance_to_pay
                    loan_cycle = LoanCycleSerializer(data=cycle)
                    loan_cycle.is_valid(raise_exception=True)
                    loan_cycle.save()
            except:
                print("Biganye")
            loan_status_dict={"data":serializer.data, "loan_cycles":cycles, "status":200, "message":"Loan disbursement successfull"}

        else:
            loan_status_dict={"status":200, "error":"Loan hasnt yet been approved or loan was already disbursed"}
        return Response(loan_status_dict, status=status.HTTP_200_OK)


class LoanCyclesView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        cycles=LoanCycles.objects.all()
        loan_group = get_object(Loans, pk)
        loan_cycles = cycles.filter(related_loan=loan_group)

        cycle_status = self.request.query_params.get('cycle_status', None)

        if cycle_status is not None:
            if cycle_status=='Pending':
                loan_cycles = loan_cycles.filter(cycle_status="Pending")
            elif cycle_status=='Paid':
                loan_cycles = loan_cycles.filter(cycle_status="Paid")

        serializer = LoanCycleListSerializer(loan_cycles, many=True)
        data_dict = {"data":serializer.data, "status":200}
        return Response(data_dict, status=status.HTTP_200_OK)

class LoanPaymentsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk ,format=None):
        loan_cycle_payment = LoanPaymentsSerializer(data=request.data)
        #get loan cycle
        related_loan_cycle = get_object(LoanCycles, pk)
        #get total loan cycles
        loan_id=related_loan_cycle.related_loan.id
        total_cycles = LoanCycles.objects.filter(related_loan=loan_id).filter(cycle_status="Unpaid")
    
        if loan_cycle_payment.is_valid():
            if total_cycles.count() > 1:
                #check prevailing cycle status
                if related_loan_cycle.cycle_status == "Unpaid":
                    loan_cycle_payment.save(related_loan_cycle=related_loan_cycle, transaction_status=True)

                    balance=calculate_balance(related_loan_cycle.amount_expected, int(request.data['amount_paid']))
                    loan_balance=related_loan_cycle.loan_balance - int(request.data['amount_paid'])
                    if balance > 0:
                        cycle_status = 'Unpaid'
                    else:
                        cycle_status = 'Paid'
                
                    cycle_update={'amount_paid':request.data['amount_paid'], 'balance':balance, 'loan_balance':loan_balance, 'cycle_status':cycle_status, 'amount_expected':balance}
                    
                    #update loan cycle with new defaults on payment
                    LoanCycles.objects.update_or_create(
                        id=pk, defaults=cycle_update)
                    

                    data_dict = {"status":201, "message":"Payment made successfully", "data":loan_cycle_payment.data, "cycle_detail":cycle_update}
                    return Response(data_dict, status=status.HTTP_201_CREATED)
                else:
                    loan_cycle_payment.save(related_loan_cycle=related_loan_cycle, comment="Transaction Failed")
                    data_dict = {"status":400, "message":"Payment was not made to cycle because cycle is fully paid out", "data":loan_cycle_payment.data}
                    return Response(data_dict, status=status.HTTP_400_BAD_REQUEST)
            else:
                #code to implement the cycle and loan completion if the payment is complete 
                pass
        return Response(loan_cycle_payment.errors, status=status.HTTP_400_BAD_REQUEST)