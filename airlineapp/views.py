from django.shortcuts import render
from django.http import HttpResponse
from .models import Trip,Food_Name,Route,Passenger,Plane
from rest_framework import viewsets
from rest_framework import permissions
from airlineapp.serializers import TripSerializer,FoodNameSerializer,RouterSerializer,PassengerSerializer,PlaneSerializer
# Create your views here.
def index(request):
    return HttpResponse("Welcome to the Airline Application!")

#API endpoint for REST framework

class RouterViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Routes
    """
    queryset = Route.objects.all()
    serializer_class = RouterSerializer

class PlaneViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Planes
    """
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer

class TripViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Trips
    """
    
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
        

class FoodViewSet(viewsets.ModelViewSet):
    """
    API endpoint for FoodNames
    """
    queryset = Food_Name.objects.all()
    serializer_class = FoodNameSerializer


class PassengerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for passengers
    """
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer


