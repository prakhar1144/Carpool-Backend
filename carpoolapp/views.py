from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import CreateRideSerializer, RideSerializer, UpdateRideSerializer
from .models import Ride

# POST
class CreateRideAPIView(CreateAPIView):
    '''
    Create a New Ride
    '''
    permission_classes = [IsAuthenticated]
    queryset = Ride.objects.all()
    serializer_class = CreateRideSerializer

# GET
class ListRideAPIView(ListAPIView):
    '''
    List of all the rides
    '''
    authentication_classes = []   
    permission_classes = [AllowAny]
    queryset = Ride.objects.all() # will be queried on the basis of departure time
    serializer_class = RideSerializer

# GET : /url/2
class DetailsRideAPIView(RetrieveAPIView):
    '''
    Info Regarding a particular Ride
    '''
    permission_classes = [AllowAny]
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

# PUT : /url/2 
class UpdateRideAPIView(UpdateAPIView):
    '''
    To join a Ride
    '''
    permission_classes = [IsAuthenticated]
    queryset = Ride.objects.all()
    serializer_class = UpdateRideSerializer
