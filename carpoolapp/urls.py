from django.urls import path
from .views import CreateRideAPIView, ListRideAPIView, DetailsRideAPIView, UpdateRideAPIView

urlpatterns = [
    path('create/', CreateRideAPIView.as_view()),
    path('list/', ListRideAPIView.as_view()),
    path('detail/<int:pk>',DetailsRideAPIView.as_view()),
    path('join/<int:pk>',UpdateRideAPIView.as_view()),
]