from accounts.models import User
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from accounts.serializers import TokenSerializer, UserSerializer, UserDetailSerializer
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from institution.models import Institution, InstitutionStaff

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            token_serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            token_serializer.is_valid()
            user_serializer = UserDetailSerializer(user)
            if user.is_institution_administrator == True:
                try:
                    related_institution = Institution.objects.get(created_by=user)
                    institution = {"id":related_institution.pk, "institution_status":related_institution.is_institution_active}
                except:
                    institution = {"status":"No institution created yet"}
            elif user.is_loan_officer == True:
                institution_staff = InstitutionStaff.objects.get(user_id=user)
                assigned_institution = Institution.objects.get(id=institution_staff.institution_id.pk)
                institution = {"id":assigned_institution.pk, "institution_status":assigned_institution.is_institution_active}
            elif user.is_teller == True:
                institution_staff = InstitutionStaff.objects.get(user_id=user)
                assigned_institution = Institution.objects.get(id=institution_staff.institution_id.pk)
                institution = {"id":assigned_institution.pk, "institution_status":assigned_institution.is_institution_active}
            login_data = {"user_data":user_serializer.data, "token_data":token_serializer.data, "institution":institution}
            return Response(login_data)
        return Response(status=status.HTTP_404_NOT_FOUND)
