from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import CreateRideSerializer, RideSerializer, UpdateRideSerializer
from .models import Ride

# POST
class CreateRideAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ride.objects.all()
    serializer_class = CreateRideSerializer

# GET
class ListRideAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Ride.objects.all() # will be queried on the basis of departure time
    serializer_class = RideSerializer

# GET : /url/2
class DetailsRideAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

# PUT : /url/2 
class UpdateRideAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ride.objects.all()
    serializer_class = UpdateRideSerializer
