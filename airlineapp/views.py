from django.shortcuts import render
from django.http import HttpResponse
from .models import Trip,Food_Name,Route,Passenger
from rest_framework import viewsets
from rest_framework import permissions
from airlineapp.serializers import TripSerializer,FoodNameSerializer,RouterSerializer,PassengerSerializer
# Create your views here.
def index(request):
    return HttpResponse("Welcome to the Airline Application!")

#API endpoint for REST framework

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

class RouterViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Routes
    """
    queryset = Route.objects.all()
    serializer_class = RouterSerializer

class PassengerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for passengers
    """
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer


