from django import http
import jwt, datetime
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from Carpool import settings
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status
from rest_framework.response import Response
from .models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CreateAccountSerializer, ForgotPasswordSerializer, SignUpSerializer, LoginSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework_simplejwt.tokens import RefreshToken


class CreateAccountAPIView(GenericAPIView):
    '''
    Click on the link received on mail after signUp to create an account.
    '''
    authentication_classes = []
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = CreateAccountSerializer

    @extend_schema(parameters=[
        OpenApiParameter('token', type=OpenApiTypes.STR, required=True)
    ])
    def get(self, request):
        token = request.GET.get('token', None)
        try:
            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            serializer = self.serializer_class(data={'email': decoded_data['email'], 'password': decoded_data['password']})
            
            if serializer.is_valid():
                serializer.save()
                token = serializer.instance.get_token()
                return Response(token , status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except jwt.ExpiredSignatureError:
            return Response({"message": "Link has expired, signIn again."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except jwt.DecodeError:
            return Response({"message": "Invalid token"}, status=status.HTTP_406_NOT_ACCEPTABLE)

class SignUpAPIView(GenericAPIView):
    '''
    Enter Your Email-Password and click on the received link on mail to create account. 
    '''
    authentication_classes = []
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer # helps in schema generation + verifies that email provided is valid + verifies if user already exists 

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            token = jwt.encode(
                {"email": data['email'],"password":data["password"], "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=86400),},
                settings.SECRET_KEY, algorithm="HS256")

            current_site = get_current_site(request).domain
            relative_link = "/register/"
            abs_url = 'https://' + current_site + relative_link + "?token=" + str(token)
            print(str(token))
            email_body = 'Hi ' + data['email'] + ' Click the below link to confirm your account ' + abs_url
            mail = {
                'email_subject': "Verify Mail",
                'email_body': email_body,
                'email': data["email"]
            }
            return Response({"message":"Check your mail", 'mail': mail}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class LoginAPIView(GenericAPIView):
    '''
    login using email pass, if valid return token else error message
    '''
    authentication_classes = []
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            print(user)
            if user is None:
                return Response({"Message":"Invalid email/Pass"}, status.HTTP_400_BAD_REQUEST)
            else:
                token = user.get_token()
                return Response(token, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class ForgotPasswordAPIView(GenericAPIView):
    permission_classes = [AllowAny,]
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = User.objects.filter(email=data['email'])[0]
            if user:
                # send a link via mail which takes user to put method
                token = jwt.encode(
                    {"user_id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=86400),},
                    settings.SECRET_KEY, algorithm="HS256")

                current_site = get_current_site(request).domain
                relative_link = "/reset"
                abs_url = 'https://' + current_site + relative_link + "?token=" + str(token)

                email_body = 'Hi ' + data['email'] + ' Click the below link to reset password ' + abs_url
                mail = {
                    'email_subject': "Reset Password",
                    'email_body': email_body,
                    'email': data["email"]
                }
                return Response({"message":"Check your mail", 'mail': mail}, status=status.HTTP_200_OK)
            else:
                return Response({"Message":"No user is registered with that mail"}, status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
 
    @extend_schema(parameters=[
        OpenApiParameter('token', type=OpenApiTypes.STR, required=True)
    ])
    def get(self, request):
        token = request.GET.get('token', None)
        try:
            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            serializer = self.serializer_class(data={'user_id': decoded_data['user_id']})
            
            if serializer.is_valid():
                secret_msg = settings.SECRET_KEY
                return Response({'user_id':serializer.validated_data['user_id'], 'secret_code':secret_msg}, status.HTTP_200_OK) # take this user id and redirect to 'PUT' with new_password for update
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except jwt.ExpiredSignatureError:
            return Response({"message": "Link has expired, Try again."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except jwt.DecodeError:
            return Response({"message": "Invalid token"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            secret_code = data['secret_code']

            if secret_code != settings.SECRET_KEY:
                return Response({"message":"Invalid Secret Code"}, status.HTTP_403_FORBIDDEN)

            user = User.objects.get(id=data["user_id"])
            user.set_password(data["new_password"])
            user.save()
            return Response({"message":"password changed"}, status.HTTP_200_OK)
        else:   
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)