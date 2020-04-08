"""
This module contains compute logic that is used in views.
This provides a logical separation of control logic with views
"""
from functools import lru_cache
from airlineapp.models import Booking
##Add caching funtionality on this function
##Might be required to send the object in json instead of a list
##Reference: https://medium.com/better-programming/every-python-programmer-should-know-lru-cache-from-the-standard-library-8e6c20c6bc49
@lru_cache(maxsize=None)
def get_seats(max_row,max_col):
        """
        Sample request get_seats(5,3)

        Sample response:
        [
    "A1",
    "A2",
    "A3",
    "B1",
    "B2",
    "B3",
    "C1",
    "C2",
    "C3",
    "D1",
    "D2",
    "D3",
    "E1",
    "E2",
    "E3"
]
"""
        row_map = {1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',
        10:'J',11:'K',12:'L',13:'M',14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',20:'T',
        21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'}
        alphabets = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        max_row = row_map.get(max_row)
        temp = []
        seats = []
        for alphabet in alphabets:
            temp.append(alphabet)
            if alphabet == max_row:
                break
        for i in range(1,max_col+1):
            for alphabet in temp:
                seats.append(f"{alphabet}{i}")
            seats.sort()
        return seats

#caching function should NOT be added on this function as the function internally 
#calls booking
def get_taken_seats(trip_id):
    """
    Sample request: Trip_id = 91
    At the time of writing this comment, two booking exist with trip_id = 91
    we return 
    Taken seats: ['A1', 'A2']
    """
    taken_seats = []
    booking_queryset = Booking.objects.all()
    for obj in booking_queryset:
        if obj.trip_id.id == trip_id:
            taken_seats.append(obj.passenger_id.seat_number)
    return taken_seats


def get_passengers(trip_id):
    """
    Returns the list of passenger IDs who have chosen a particular trip_id
    """
    passengers = []
    booking_queryset = Booking.objects.all()
    for obj in booking_queryset:
        if obj.trip_id.id == trip_id:
            passengers.append(obj.passenger_id.id)
    return passengers

def send_notification(email):
    """
    Helper function to send a notification email to passengers
    """
    pass