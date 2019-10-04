from rest_framework import generics
from django.http import QueryDict

from .models import LoanGroup, GroupMember, SavingsAccount, SharesAccount, SavingsPayments
from institution.models import InstitutionSettings
from .serializers import LoanGroupSerializer, GroupMemberSerializer, GroupMemberListSerializer, MemberPaymentsSerializer, SavingsAccountSerializer, SharesAccountSerializer, SharesPaymentsSerializer, SavingsPaymentsSerializer, MemberSavingsPaymentsSerializer, SavingsWithdrawalSerializer, AccountNumberSerializer
from accounts.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from accounts.models import User

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework import permissions
from helpers.helpers import get_object, generate_account_number, send_sms
from accounts.permissions import BranchManagerPermissions, LoanClientPermissions, LoanOfficerPermissions, TellerPermissions
from django.conf import settings

import urllib.request
import json

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

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        data_dict = {"status":200, "data":serializer.data}
        return Response(data_dict, status=status.HTTP_200_OK)

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


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user_detail = self.get_object(pk)
        serializer = UserSerializer(user_detail)
        # data_with_link = dict(serializer.data)#["member"] = 'groups/{}/members/'.format(pk)
        # links = {'members': 'api/v1/groups/{}/members/'.format(pk)}
        # data_with_link['links'] = links
        data_dict = {"data":serializer.data, "status":200}
        return Response(data_dict, status=status.HTTP_200_OK)    

class MemberFeesPayment(APIView):
    """
    Get the member fees to be paid on registration
    """
    permission_classes = (permissions.IsAuthenticated, LoanOfficerPermissions)

    def get(self, request, pk, format=None):
        group = get_object(LoanGroup, pk)
        institution_settings = get_object(InstitutionSettings, group.institution_id.pk)
        payment_serializer = MemberPaymentsSerializer(institution_settings)
        data_dict = {"fees_to_pay":payment_serializer.data, "status":200}
        return Response(data_dict, status=status.HTTP_200_OK)


class MemberList(APIView):
    """
    List all members and create a new member.
    """
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request, format=None):
        members = GroupMember.objects.all()
        serializer = GroupMemberListSerializer(members, many=True)
        data_dict = {"status":200, "data":serializer.data}
        return Response(data_dict, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        member_data = request.data.copy()
        # try:
        username    = member_data.pop('username', None)
        first_name  = member_data.pop('first_name', None)
        last_name   = member_data.pop('last_name', None)
        email       = member_data.pop('email', None)
        password    = member_data.pop('password', None)

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

        #add query dict to user serializer
        member_serializer = GroupMemberSerializer(data=member_data)
        if member_serializer.is_valid():
            user_account_serializer = UserSerializer(data=user_data_query_dict)
            user_account_serializer.is_valid(raise_exception=True)
            user_account_serializer.save()

            user = User.objects.get(pk=user_account_serializer.data['id'])

            member_serializer.save(user_id=user)
            #create savings and shares accounts
            savings_account_number = generate_account_number(member_serializer.data['id'], "savings")
            savings_account = {
                'group_member_related':member_serializer.data['id'],
                'account_number': savings_account_number
                #'account_balance':member_serializer.data[''],
                #'running_balance':0,
                #'interest_accrued':0
            }
            savings_account_creation = SavingsAccountSerializer(data=savings_account)
            savings_account_creation.is_valid(raise_exception=True)
            savings_account_creation.save()

            #create shares account
            shares_account_number = generate_account_number(member_serializer.data['id'], 'shares')
            shares_account = {
                'group_member_related':member_serializer.data['id'],
                'account_number': shares_account_number,
                'account_balance': member_serializer.data['shares_fee'],
                'running_balance': member_serializer.data['shares_fee'],
                #'interest_accrued':0
            }
            shares_account_creation = SharesAccountSerializer(data=shares_account)
            shares_account_creation.is_valid(raise_exception=True)
            shares_account_creation.save()

            #send twilio sms with registration details
            phone_number = "{}{}".format(member_serializer.data['phone_dialing_code'], member_serializer.data['phone_number'])
            message = "Welcome to MFI, Savings account Number is {} with balance of {}, Shares Account Number is {} with balance of {} shs".format(savings_account_number, 0, shares_account_number, 0)
            try:
                send_sms(phone_number, message)
            except:
                print("Message Not sending")
            data_dict = {"status":201, "data":member_serializer.data, "savings_account":savings_account, "shares_account":shares_account}
            return Response(data_dict, status=status.HTTP_201_CREATED)
            # except:
            #     print("Failed")
            #     # return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
        savings_account = SavingsAccount.objects.get(group_member_related=group_member)
        shares_account = SharesAccount.objects.get(group_member_related=group_member)
        serializer = GroupMemberListSerializer(group_member)
        savings_serializer = SavingsAccountSerializer(savings_account)
        shares_serializer = SharesAccountSerializer(shares_account)
        data_with_link = dict(serializer.data)
        links = {'loans': 'api/v1/members/{}/loans/'.format(pk)}
        data_with_link['links'] = links
        data_with_link["savings_account"] = savings_serializer.data
        data_with_link["shares_account"] = shares_serializer.data
        data_dict = {"status":200, "data":data_with_link}
        return Response(data_dict, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        group_member = self.get_object(pk)
        serializer = GroupMemberListSerializer(group_member, data=request.data)
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
        serializer = GroupMemberSerializer(group_members, many=True)
        data_dict = {"status":200, "data":serializer.data}
        return Response(data_dict, status=status.HTTP_200_OK)


class SavingsToBePaid(APIView):
    """
    Return amount of money to be paid and next payment date.
    """
    permissions_classes = (permissions.IsAuthenticated, LoanOfficerPermissions)
    def get(self, request, pk, format=None):
        group = get_object(LoanGroup, pk)
        institution_settings = get_object(InstitutionSettings, group.institution_id.pk)
        savings_payment_expected = MemberSavingsPaymentsSerializer(institution_settings)
        data_dict = {"amount_to_pay":savings_payment_expected.data, "status":200}
        return Response(data_dict, status=status.HTTP_200_OK)

class CheckAccountBalances(APIView):
    pass

class SavingsAccountList(APIView):
    """
    List all savings accounts
    """
    permission_classes = (permissions.IsAuthenticated, LoanOfficerPermissions)

    def get(self, request, format=None):
        accounts = SavingsAccount.objects.all()
        serializer = SavingsAccountSerializer(accounts, many=True)
        data_dict = {"status":200, "data":serializer.data}
        return Response(data_dict, status=status.HTTP_200_OK)


class SavingsPaymentList(APIView):
    """
    List and create savings payments
    """
    permission_classes = (permissions.IsAuthenticated, TellerPermissions)

    def post(self, request, format=None):
        savings_data = request.data.copy()
        payment_method = savings_data.pop('payment_method', None)
        phone_number   = savings_data.pop('phone_number', None)

        savings_payment_serializer = SavingsPaymentsSerializer(data=savings_data)
        if savings_payment_serializer.is_valid():
            if payment_method[0] == "CASH":
                savings_payment_serializer.save()
                #add amount to savings account
                savings_account = get_object(SavingsAccount, savings_payment_serializer.data['savings_account_related'])

                saving_amount_update = {
                    "account_balance": float(savings_account.account_balance)+float(savings_payment_serializer.data['amount_paid']),
                    "running_balance": float(savings_account.running_balance)+float(savings_payment_serializer.data['amount_paid']),
                }

                SavingsAccount.objects.update_or_create(
                            id=savings_account.pk, defaults=saving_amount_update)

                savings_account_updated = get_object(SavingsAccount, savings_account.pk)

                #send twilio sms with payment details
                phone_number = "{}{}".format(savings_account.group_member_related.phone_dialing_code, savings_account.group_member_related.phone_number)
                message = "You have deposited {} on Savings account Number {}. Your Balance is {}".format(savings_payment_serializer.data['amount_paid'], savings_account_updated.account_number, savings_account_updated.account_balance)
                try:
                    send_sms(phone_number, message)
                except:
                    print("Message Not sending")

                data_dict = {"status":201, "data":savings_payment_serializer.data, "savings_account": savings_account_updated.account_balance}
                return Response(data_dict, status=status.HTTP_201_CREATED)
            else:
                savings_payment_serializer.save()
                #add amount to savings account
                savings_account = get_object(SavingsAccount, savings_payment_serializer.data['savings_account_related'])

                saving_amount_update = {
                    "account_balance": float(savings_account.account_balance)+float(savings_payment_serializer.data['amount_paid']),
                    "running_balance": float(savings_account.running_balance)+float(savings_payment_serializer.data['amount_paid']),
                }

                SavingsAccount.objects.update_or_create(
                            id=savings_account.pk, defaults=saving_amount_update)

                savings_account_updated = get_object(SavingsAccount, savings_account.pk)

                data = {
                    "service_code":"M002",
                    "merchant_phone_number":phone_number[0],
                    "client_phone_number":phone_number[0],
                    "amount":"2000",
                    "reason":"Savings Payment"
                }

                body = str.encode(json.dumps(data))

                url = '{}/api/v1/payments/service_payment/'.format(settings.PAY_URL)
                # api_key = '7/1GTEPNjebtQ4Oq3kLFZyYoXhivqCxBKbfg0L0Q6yA80oGop2s/BzWdxmUzJv8yQERZ5NKvqDzx8j8AEh6xWQ==' # Replace this with the API key for the web service
                headers = {'Content-Type':'application/json'}

                req = urllib.request.Request(url, body, headers)

                try:
                    response = urllib.request.urlopen(req)

                    result = response.read()
                    #decode result from binary string to dictionary
                    decoded_result=json.loads(result.decode())
                    print(decoded_result)
                    # scored_label = decoded_result['Results']['output1'][0]['Scored Labels']
                    # print(scored_label)
                except urllib.error.HTTPError as error:
                    print("The request failed with status code: " + str(error.code))

                # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
                    print(error.info())
                    print(json.loads(error.read().decode("utf8", 'ignore')))

                #send twilio sms with payment details
                phone_number = "{}{}".format(savings_account.group_member_related.phone_dialing_code, savings_account.group_member_related.phone_number)
                message = "You have deposited {} on Savings account Number {}. Your Balance is {}".format(savings_payment_serializer.data['amount_paid'], savings_account_updated.account_number, savings_account_updated.account_balance)
                try:
                    send_sms(phone_number, message)
                except:
                    print("Message Not sending")

                data_dict = {"status":201, "data":savings_payment_serializer.data, "savings_account": savings_account_updated.account_balance}
                return Response(data_dict, status=status.HTTP_201_CREATED)
        return Response(savings_payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SavingsPaymentDetail(APIView):
    """
    Get savings payment by user/member id
    """
    permissions_classes = (permissions.IsAuthenticated, LoanOfficerPermissions)

    def post(self, request):
        account_details = AccountNumberSerializer(data=request.data)
        if account_details.is_valid():
            account_number = SavingsAccount.objects.get(account_number=account_details.data['account_number'])
            print(account_number)
            savings_payment_history = SavingsPayments.objects.filter(savings_account_related=account_number)
            savings_payments_history_serializer = SavingsPaymentsSerializer(savings_payment_history ,many=True)
            data_dict = {"savings_payments_history":savings_payments_history_serializer.data, "status":200}
            return Response(data_dict, status=status.HTTP_200_OK)
        return Response(account_details.errors, status=status.HTTP_400_BAD_REQUEST)


class SavingsWithdrawal(APIView):
    """
    Withdraw savings from account
    """
    permission_classes = (permissions.IsAuthenticated, TellerPermissions)

    def post(self, request):
        withraw_data = request.data.copy()
        account_number = withraw_data.pop('account_number')
        savings_account_related = SavingsAccount.objects.get(account_number=account_number[0])

        savings_withdrawal_serilizer = SavingsWithdrawalSerializer(data=request.data)
        if savings_withdrawal_serilizer.is_valid():
            savings_withdrawal_serilizer.save(savings_account_related=savings_account_related)

            saving_amount_update = {
                "account_balance": float(savings_account_related.account_balance)-float(savings_withdrawal_serilizer.data['amount_withdrawn']),
                "running_balance": float(savings_account_related.running_balance)-float(savings_withdrawal_serilizer.data['amount_withdrawn']),
            }

            SavingsAccount.objects.update_or_create(
                        id=savings_account_related.pk, defaults=saving_amount_update)

            savings_account_updated = get_object(SavingsAccount, savings_account_related.pk)

            #send twilio sms with payment details
            phone_number = "{}{}".format(savings_account_related.group_member_related.phone_dialing_code, savings_account_related.group_member_related.phone_number)
            message = "You have withdrawn {} from Savings account Number {}. Your Balance is {}".format(savings_withdrawal_serilizer.data['amount_withdrawn'], savings_account_updated.account_number, savings_account_updated.account_balance)
            try:
                send_sms(phone_number, message)
            except:
                print("Message Not sending")

            data_dict = {"status":200, "data":savings_withdrawal_serilizer.data, "savings_account": savings_account_updated.account_balance}
            return Response(data_dict, status=status.HTTP_201_CREATED)
        else:
            savings_withdraw_dict={"status":400, "error":savings_withdrawal_serilizer.errors}
        return Response(savings_withdraw_dict, status=status.HTTP_200_OK)


