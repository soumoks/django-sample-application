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
from airlineapp.services import get_seats,get_taken_seats
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

    
# class ValidSeatsViewSet(viewsets.ModelViewSet):
#     """
#     Returns all booking objects that match the trip id
#     TODO: Try to parse the passenger objects rather than returning all the booking objects
#     """
#     serializer_class = BookingSerializer

#     def get_queryset(self):
#         queryset = Booking.objects.all()
#         #We will get the trip id from the front end
#         trip_id = self.request.query_params.get('trip_id')
#         print(f"Trip ID: {trip_id}")
#         if trip_id is not None:
#             #select Bookings with same Trip ID (passed in queryString)
#             queryset = queryset.filter(trip_id=trip_id)
#             return queryset
#         else:
#             empty_list = []
#             return empty_list
     
class SearchBookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer

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


@api_view(['GET'])
def get_total_seats(request):
    """
    API endpoint for getting available seats on plane
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
    Accepts a trip_id as a parameter or plane_id as a parameter
    check the total_seats in the plane_id by calling the helper get_seats function
    check the booking table with seat_names for that trip_id
    """
    #query strings are string type
    #database objects are whatever are stored inside the db
    trip_id = int(request.query_params.get('trip_id'))
    if trip_id is not None:
        try:
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

class BookingViewSet(APIView):
    """
    API endpoint for Make Booking
    """
    # queryset = Booking.objects.all()
    # serializer_class = BookingSerializer

    def get(self, request, format=None):
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    #parser_classes = [JSONParser]
    """
    Request:
    headers: Content-type: application/json
            {
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
    "fname": "Sourabh",
    "lname": "Mokhasi",
    "age": 24,
    "sex": "M",
    "seat_number": "A1",
    "food_name": {
      "id": 1,
      "food_name": "Veg"
    }
  },
  "book_type": "One-Way"
}
    """

    def post(self, request, format=None):
        serializer = BookingSerializer(data=request.data)
        print("request data: ", request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def create_food(request):
    """
    Sample curl request
    curl -X POST http://127.0.0.1:8000/airline/createfood -H 'Content-Type: application/json' --data '{"food_name":"EggSalad"}'
    """
    if request.method == 'POST':
        print("HelloWorld")
        print("request data: ", request.data)
        serializer = FoodNameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_passenger(request):
    """
    Sample request:
    curl -X POST http://127.0.0.1:8000/airline/createpassenger -H 'Content-Type: application/json' --data '{"fname":"Harvey","lname":"Specter","age":34,"sex":"M","seat_number":"A3","food_name":1}'
    """
    print(f"request data: {request.data}")
    serializer = PassengerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def create_booking(request):
    """
    Sample request:
     curl -X POST http://127.0.0.1:8000/airline/createbooking -H 'Content-Type: application/json' --data '{"book_type":"One-Way","trip_id":202,"passenger_id":{"fname":"Mike","lname":"Ross","age":20,"sex":"M","seat_number":"C2","food_name":1}}
    """
    if request.method == 'POST':
        print(f"request data: {request.data}")
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)