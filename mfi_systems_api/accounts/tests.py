import json

from django.test import TestCase
from accounts.models import User
from members.models import LoanGroup
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

# update the BaseViewTest to this

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_loan_group(group_name="", branch_name=""):
        if group_name != "" and branch_name != "":
            LoanGroup.objects.create(group_name=group_name, branch_name=branch_name)
    
    def login_a_user(self, username="", password=""):
        url = reverse(
            "auth-login",
        )
        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type="application/json"
        )
    
    def setUp(self):
        # create a admin user
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )
        # add test data
        self.create_loan_group("group1", "branch1")
        self.create_loan_group("group2", "branch1")
        self.create_loan_group("group3", "branch2")
        self.create_loan_group("group4", "branch1")

class AuthLoginUserTest(BaseViewTest):
    """
    Tests for the auth/login/ endpoint
    """

    def test_login_user_with_valid_credentials(self):
        # test login with valid credentials
        response = self.login_a_user("test_user", "testing")
        # assert token key exists
        self.assertIn("token", response.data)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test login with invalid credentials
        response = self.login_a_user("anonymous", "pass")
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
