"""
This module contains compute logic that is used in views.
This provides a logical separation of control logic with views
"""
from functools import lru_cache
from airlineapp.models import Booking
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .models import *
try:
    import credentials
except:
    print("Credentials file not found. Defaulting to OS environment variables")
import json
import os

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
            passenger = Passenger.objects.get(id=obj.passenger_id.id)
            passengers.append(passenger)
    return passengers

def _generate_message(message_type,passenger,message=None):
    fname = str(passenger.fname)
    lname = str(passenger.lname)

    def update_message():
        subject = "Notification of Flight update"
        content = "Dear "+ fname + " " + lname +": \n"+"Your flight has been updated"
        return (subject,content)
    def booking_message():
        subject = "Notification of Flight booking"
        if message is not None:
            content = "Dear "+ fname + " " + lname +": \n"+"Thank you for your booking. We look forward to having you on-board." + "\n" + "Your booking reference number is:" + message
        else:
            #Fail to a default message if message is not passed for whatever reason
            content = "Dear "+ fname + " " + lname +": \n"+"Thank you for your booking. We look forward to having you on-board."
        return (subject,content)
    def cancel_message():
        subject = "Notification of cancelled flight"
        content = "Dear "+ fname + " " + lname +": \n"+" Please note that the flight that you have recently booked has been cancelled. Please visit our website to book another flight.\n Thank you for your patience and understanding."
        return (subject,content)
    def self_cancel_message():
        subject = "Notification of cancelled flight"
        content = "Dear "+ fname + " " + lname +": \n"+" Your flight has been cancelled"
        return (subject,content)

    message_map = {"book":booking_message(),"update":update_message(),"cancel":cancel_message(),"self-cancel":self_cancel_message()}
    return message_map.get(message_type,"Nothing")


def send_notification(passenger,message_type,message=None):
    """
    Helper function to send a notification email to passengers
    """
    send_grid_key = ""
    try:
        send_grid_key = credentials.get_sendgrid_key()
    except:
        #Obtain the api_key from EB environment variables
        #reference:https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-softwaresettings.html
        send_grid_key = os.environ['SENDGRID_API_KEY']

    #If the email field has not been filled for the passenger, hardcoded value for email is used for testing purposes
    print(f"Passenger data in send notification: {type(passenger)}")
    #Fail if the passed passenger object is not of type airlineapp.models.Passenger
    if isinstance(passenger,Passenger):
        if passenger.email is not None:
            email = str(passenger.email)
            subject,content = _generate_message(message_type,passenger,message)
        
            message = Mail(
                from_email='airlinereservation@sourabh.org',
                to_emails=email,
                subject=subject,
                html_content=content)
            
            try:
                sg = SendGridAPIClient(send_grid_key)
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)

            except Exception as e:
                print("Something went wrong!")
        else:
            print("Failed to send email as email is not present in Passenger object")
    else:
        print("Failed to send message as instance type passed in not Passenger")