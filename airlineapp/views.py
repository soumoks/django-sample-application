from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from airlineapp.serializers import *
from rest_framework.parsers import JSONParser
from airlineapp.services import get_seats,get_taken_seats, send_notification
from rest_framework.decorators import api_view

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
        return_route_id = self.request.query_params.get('return_route_id')
        return_date = self.request.query_params.get('return_date')
        print(f"depart_date:{depart_date}")
        print(f"Route ID: {route_id}")
        #If return_date and return_route_id is supplied in request
        if depart_date and route_id and return_date and return_route_id is not None:
            #Check both trips for requested route_ids in DB 
            queryset1 = queryset.filter(route_id=route_id).filter(date=depart_date)
            queryset2 = queryset.filter(route_id=return_route_id).filter(date=return_date)
            queryset = queryset1 | queryset2
            return queryset
        #If depart_date and route_id are provided in request
        if depart_date and route_id is not None:
            #select * from trips whre route_id=182 and date = 2020-04-02
            queryset = queryset.filter(route_id=route_id).filter(date=depart_date)
            return queryset
        if route_id is not None:
            queryset = queryset.filter(route_id=route_id)
            return queryset
        #If no matches
        else:
            empty_list = []
            return empty_list


     
class SearchBookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSearchSerializer

    """
    API endpoint for getbookings
    Accepts trip_id or booking_id as query params
    
    Sample query:
    http://127.0.0.1:8000/airline/getbookings?booking_id=1
    http://127.0.0.1:8000/airline/getbookings?trip_id=91

    Sample response:
    [
    {
        "id": 1,
        "trip_id": {
            "id": 91,
            "route_id": {
                "id": 115,
                "departure_city": "Montreal - YUL",
                "arrival_city": "Edmonton - YEG"
            },
            "plane_id": {
                "id": 13,
                "company": "Lee, King and Patterson",
                "model_no": 76272,
                "capacity": 281,
                "max_row": 35,
                "max_col": 7
            },
            "date": "2020-04-06",
            "arrival_time": "07:58:45",
            "departure_time": "14:46:50"
        },
        "passenger_id": {
            "id": 1,
            "food_name": {
                "id": 1,
                "food_name": "Veg"
            },
            "fname": "Sourabh",
            "lname": "Mokhasi",
            "age": 24,
            "sex": "M",
            "seat_number": "A1"
        },
        "book_type": "One-Way"
    }
    ]
    """
    
    def get_queryset(self):
        #return all bookings which match the id passed from front end
        queryset = Booking.objects.all()
        booking_id = self.request.query_params.get('booking_id')
        trip_id = self.request.query_params.get('trip_id')
        if booking_id is not None:
            queryset=queryset.filter(id=booking_id)
            return queryset
        elif trip_id is not None:
            #select Bookings with same Trip ID (passed in queryString)
            queryset = queryset.filter(trip_id=trip_id)
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

class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

class FeatureNameViewSet(viewsets.ModelViewSet):
    queryset = Feature_Name.objects.all()
    serializer_class = FeatureNameSerializer



@api_view(['GET'])
def get_total_seats(request):
    """
    API endpoint for 'getseats' on plane
    Should return total seats available on plane as an array
    Sample response = 
    [A1,A2,A3,B1,B2,B3]

    Should also return available seats that are not assigned to passengers in Booking
    Sample response =
    [A1,A2,A3]
    accepts plane_id as query param
    """
    plane_id = request.query_params.get('plane_id')
    if plane_id is not None:
        try:
            queryset = Plane.objects.get(id=plane_id)
            # print(f"max_row: {queryset.max_row} | max_col: {queryset.max_col}")
            # print("Available seats:")
            # print(get_seats(queryset.max_row,queryset.max_col))
            return Response(get_seats(queryset.max_row,queryset.max_col))
        except:
            return Response("Plane not found")
    else:
        empty_list = []
        return Response(empty_list)



@api_view(['GET'])
def get_available_seats(request):
    """
    API endpoint for "getavailseats"
    Accepts a trip_id as a parameter or plane_id as a parameter
    check the total_seats in the plane_id by calling the helper get_seats function
    check the booking table with seat_names for that trip_id
    """
    #query strings are string type
    #database objects are whatever are stored inside the db
    trip_id = request.query_params.get('trip_id')
    if trip_id is not None:
        try:
            #Convert to int for query
            trip_id = int(trip_id)
            trip_queryset = Trip.objects.get(id=trip_id)

            #get total seats
            total_seats = []
            plane_id = trip_queryset.plane_id
            total_seats = get_seats(plane_id.max_row,plane_id.max_col)
            print(f"Total seats: {total_seats}")

            #get taken seats
            taken_seats = []
            taken_seats = get_taken_seats(trip_id)
            print(f"Taken seats: {taken_seats}")

            #get available seats
            #compute difference of total_seats and taken_seats
            available_seats = []
            available_seats = list(set(total_seats) - set(taken_seats))
            available_seats.sort()
            print(f"Available seats: {available_seats}")
            return Response(available_seats)            
        except:
            return Response("Trip not found")
    else:
        empty_list = []
        return Response(empty_list)



@api_view(['POST'])
def create_food(request):
    """
    API Endpoint for "createfood"
    Sample curl request
    curl -X POST http://127.0.0.1:8000/airline/createfood -H 'Content-Type: application/json' --data '{"food_name":"EggSalad"}'
    """
    print("request data: ", request.data)
    serializer = FoodNameSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def create_passenger(request):
    """
    API endpoint for "createpassenger"
    Sample request:
    curl -X POST http://127.0.0.1:8000/airline/createpassenger -H 'Content-Type: application/json' --data '{"fname":"Harvey","lname":"Specter","age":34,"sex":"M","seat_number":"A3","food_name":1}'
    #Added email field to passenger model
    curl -X POST http://127.0.0.1:8000/airline/createpassenger -H 'Content-Type: application/json' --data '{"fname":"Harvey","lname":"Specter","age":34,"sex":"M","seat_number":"A3","food_name":1,"email":"test@gmail.com"}'
    """
    print(f"request data: {request.data}")
    serializer = PassengerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST', 'PUT', 'DELETE'])
def create_booking(request, pk=None):
    """
    API endpoint for "createbooking"
    Sample request:
     curl -X POST http://127.0.0.1:8000/airline/createbooking -H 'Content-Type: application/json' --data '{"book_type":"One-Way","trip_id":202,"passenger_id":{"fname":"Mike","lname":"Ross","age":20,"sex":"M","seat_number":"C2","food_name":1}}'
     curl -X POST http://127.0.0.1:8000/airline/createbooking -H 'Content-Type: application/json' --data '{"book_type":"One-Way","trip_id":202,"passenger_id":12}'
     curl -X PUT http://127.0.0.1:8000/airline/createbooking -H 'Content-Type: application/json' --data '{"id":15,"book_type":"One-Way","trip_id":203,"passenger_id":170}'
     curl -X DELETE http://127.0.0.1:8000/airline/createbooking/12

     #Provide the passenger ID and it
     #For the time-being create passenger first and call create_booking
    """
    ## Create passenger object
    # if request.method == "POST" and request.data is not None:
    #     print(f"request data: {request.data}")
    #     passenger_data = request.data['passenger_id']
    #     p = create_passenger(passenger_data)
        
    #     # p = Passenger.objects.create(fname=passenger_data["fname"],lname=passenger_data["lname"],age=passenger_data["age"],sex=passenger_data["sex"],seat_number=passenger_data["seat_number"],food_name=passenger_data["food_name"])

    
    if request.method == "POST" and request.data is not None:
        passenger_data = Passenger.objects.get(id=request.data['passenger_id'])
        print(f"request data: {request.data}")
        #Getting the passenger object as it is required for send_notification
        
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #Accessing elements in a ordered dict
            #https://stackoverflow.com/questions/10058140/accessing-items-in-an-collections-ordereddict-by-index
            # passenger_data = list(serializer.validated_data.items())[2]
            # print(f"Booking reference ID: {serializer.data['id']}")
            send_notification(passenger_data,"book",str(serializer.data['id']))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT" and request.data is not None:
        passenger_data = Passenger.objects.get(id=request.data['passenger_id'])
        print(f"request data: {request.data}")
        
        try:
            booking = Booking.objects.get(id=request.data.get('id'))
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_notification(passenger_data,"update")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE" and request.data is not None:
        print(f"request data: {request.data}")
        try:
            booking = Booking.objects.get(id=pk)
            #update passenger_data for delete as we only receive Booking ID in request
            
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        passenger_data = booking.passenger_id
        booking.delete()
        send_notification(passenger_data,"self-cancel")
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

