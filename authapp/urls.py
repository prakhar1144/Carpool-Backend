from django.urls import path
from .views import CreateAccountAPIView, LoginAPIView, ForgotPasswordAPIView, SignUpAPIView

urlpatterns = [
    path('signup/', SignUpAPIView.as_view()),
    path('createaccount/', CreateAccountAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('reset/', ForgotPasswordAPIView.as_view()),
]