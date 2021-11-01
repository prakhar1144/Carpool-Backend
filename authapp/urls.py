from django.urls import path
from .views import CreateAccountAPIView, LoginAPIView, ForgotPasswordAPIView, SignUpAPIView, LogoutAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SignUpAPIView.as_view()),
    path('createaccount/', CreateAccountAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('reset/', ForgotPasswordAPIView.as_view()),
    path('token/refresh/',TokenRefreshView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
]