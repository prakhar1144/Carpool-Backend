from django.urls import path
from .views import RegisterAPIView, VerifyEmailAPIView, LoginAPIView, ForgotPasswordAPIView

urlpatterns = [
    path('', RegisterAPIView.as_view()),
    path('verify/', VerifyEmailAPIView.as_view() ,name="mail-verification"),
    path('login/', LoginAPIView.as_view()),
    path('reset/', ForgotPasswordAPIView.as_view()),
]