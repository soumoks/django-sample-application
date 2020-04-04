from django.shortcuts import render
from django.http import HttpResponse
from .models import Trip,Food_Name,Route,Passenger,Plane
from rest_framework import viewsets
# from rest_framework.request import request
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
    serializer_class = TripSerializer
    """
    Sample query:
    http://127.0.0.1:8000/airline/gettrips?route_id=182&depart_date=2020-09-26

    Response:
    [
    {
        "date": "2020-09-26",
        "arrival_time": "13:38:20",
        "departure_time": "08:01:14",
        "route_id": {
            "id": 182,
            "departure_city": "Saskatoon - YXE",
            "arrival_city": "Halifax - YHZ"
        },
        "plane_id": {
            "id": 3,
            "company": "Kelley, Jennings and Johnson",
            "model_no": 74632,
            "capacity": 282,
            "max_row": 33,
            "max_col": 3
        }
    }
    ]
    """
    def get_queryset(self):
        queryset = Trip.objects.all()
        depart_date = self.request.query_params.get('depart_date')
        route_id = self.request.query_params.get('route_id')
        print(f"depart_date:{depart_date}")
        print(f"Route ID: {route_id}")
        #If depart_date and route_id are provided in request
        if depart_date and route_id is not None:
            queryset = queryset.filter(route_id=route_id).filter(date=depart_date)
            return queryset
        #If only depart_date is supplied in request
        elif depart_date:
            queryset = queryset.filter(date=depart_date)
            return queryset
        #If no matches
        else:
            empty_list = []
            return empty_list

    
        

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


