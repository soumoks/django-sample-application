from django.shortcuts import render
from django.http import HttpResponse
from .models import Trip,Food_Name,Route,Passenger,Plane, Feature, Feature_Name, Booking
from rest_framework import viewsets
from rest_framework import status
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from airlineapp.serializers import TripSerializer,FoodNameSerializer,RouterSerializer,PassengerSerializer,PlaneSerializer, FeatureSerializer, FeatureNameSerializer, BookingSerializer
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
            #select * from trips whre route_id=182 and date = 2020-04-02
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

    
class ValidSeatsViewSet(viewsets.ModelViewSet):
    """
    Returns all booking objects that match the trip id
    TODO: Try to parse the passenger objects rather than returning all the booking objects
    """
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = Booking.objects.all()
        #We will get the trip id from the front end
        trip_id = self.request.query_params.get('trip_id')
        print(f"Trip ID: {trip_id}")
        if trip_id is not None:
            #select passenger from booking where trip id = x
            queryset = queryset.filter(trip_id=trip_id)
            return queryset
        else:
            empty_list = []
            return empty_list
     
class SearchBookingIdViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        #return all bookings which match the id passed from front end
        queryset = Booking.objects.all()
        booking_id = self.request.query_params.get('id')
        if booking_id is not None:
            queryset=queryset.filter(id=booking_id)
            return queryset
        else:
            empty_list = []
            return empty_list

            
class FoodViewSet(viewsets.ModelViewSet):
    """
    API endpoint for FoodNames
    """
    queryset = Food_Name.objects.all()
    serializer_class = FoodNameSerializer


# class PassengerViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint for passengers
#     """
#     queryset = Passenger.objects.all()
#     serializer_class = PassengerSerializer
# class PassengerList(APIView):
#     """
#     API Endpoint for get and add passengers
#     Reference:
#     https://www.django-rest-framework.org/tutorial/3-class-based-views/
#     """

#     #response on GET request
#     def get(self,request,format=None):
#         passengers = Passenger.objects.all()
#         serializer = PassengerSerializer(passengers, many=True)
#         return Response(serializer.data)
#     #response on POST request
#     def post(self, request, format=None):
#         serializer = PassengerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CancelBookingViewSet(viewsets.ModelViewSet):



class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

class FeatureNameViewSet(viewsets.ModelViewSet):
    queryset = Feature_Name.objects.all()
    serializer_class = FeatureNameSerializer

