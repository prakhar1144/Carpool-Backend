"""Carpool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from authapp.views import RegisterAPIView, VerifyEmailAPIView, LoginAPIView, ForgotPasswordAPIView
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view( # new
                openapi.Info(
                title="Carpool API",
                default_version="v1",
                description="APIs for Carpool",
                ),
            public=True,
            permission_classes=(AllowAny,),
        )

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-ui"),
    path('admin/', admin.site.urls),
    path('api/v1/', include('authapp.urls')),
    path('api/v1/', include('carpoolapp.urls')),
]
