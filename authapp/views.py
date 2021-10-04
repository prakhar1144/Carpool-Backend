from drf_spectacular.types import OpenApiTypes
import jwt, datetime

from rest_framework.views import APIView
from Carpool import settings
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status
from rest_framework.response import Response
from .models import User
from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from drf_spectacular.utils import OpenApiExample, extend_schema, OpenApiParameter, OpenApiResponse

def create_email(request, user, subject):
    
    token = jwt.encode(
        {"user_id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=86400), "subject": subject},
        settings.SECRET_KEY, algorithm="HS256")

    current_site = get_current_site(request).domain
    relative_link = reverse("mail-verification")
    abs_url = 'http://' + current_site + relative_link + "?token=" + str(token)

    email_body = 'Hi ' + user.email + ' Use link below ' + abs_url
    data = {
        'email_subject': subject,
        'email_body': email_body,
        'email': user.email
    }
    return data

class RegisterAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        serializer.save() # Modelserializer createMethod is called
        print("ok")
        user = User.objects.get(email=serializer.data['email'])

        data = create_email(self.request, user, "New Account")
        print(data)
        #send_email_task.delay(data)
        return Response({"message":"verify your mail"}, status=status.HTTP_201_CREATED)

class VerifyEmailAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        token = request.GET.get('token', None)
        try:
            data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=data['user_id'])
            subject = data["subject"]
            if subject == "New Account":
                if not user.is_verified:
                    user.is_verified = True
                    user.save()
                    return Response({"message": "Account verified successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Already activated"})
            elif subject == "Forgot Password":
                return Response({"user_id":user.id}, status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"message": "Token has expired. "}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(request=RegisterSerializer, description='Login Using Email-Pass to get Token', responses={
            200: OpenApiResponse(response=OpenApiTypes.STR , description='A JWT Token'),
            404: OpenApiResponse(response=OpenApiTypes.STR , description='Error Message')
        })
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    
    # login using email pass, if valid return token else error mssg
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            token = user.get_token()
            return Response(token, status.HTTP_200_OK)
        else:
            return Response({"Message":"Invalid email/Pass"}, status.HTTP_404_NOT_FOUND)

class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        email = request.data['email']
        user = User.objects.filter(email=email)[0]
        if user:
            # send a link via mail which takes user to put method
            data = create_email(self.request ,user, "Forgot Password")
            # send_mail()
            print(data)
            return Response({"Message":"Check Your Mail"}, status.HTTP_200_OK)
        else:
            return Response({"Message":"No user is registered with that mail"}, status.HTTP_204_NO_CONTENT)

    def put(self, request):
        new_password = request.data["password"]
        user_id = request.data["user_id"]
        print(new_password)
        print(user_id)
        user = User.objects.get(id=user_id)
        user.set_password(new_password)
        user.save()
        return Response({"message":"password changed"}, status.HTTP_200_OK)

class LogoutAPIView(APIView):
    pass
