import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','AirlineReservationSystem.settings')

import django
django.setup()

from random import randint
import random
import string

from airlineapp.models import Trip, Booking, Plane, Booking_Type, Route, Food_Name, Passenger, Feature, Feature_Name
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker
from itertools import permutations
from datetime import date, timedelta

fake = Faker()

def create_passenger(n=50):
    sex_type = ['M','F']
    for _ in range (n):
        name = fake.name()
        fname = name.split()[0]
        lname = name.split()[1]
        age = randint(1,100)
        sex = random.choice(sex_type)
        seat_rows=['1','2','3','4','5']
        seat_cols=['A','B','C']
        seat_list = [random.choice(seat_cols),random.choice(seat_rows)]
        seat_num = "".join(seat_list)
        food_num = random.choice(Food_Name.objects.all())
        Passenger.objects.create(fname = fname, lname = lname, age = age, sex = sex, seat_number = seat_num, food_name = food_num)
        
def create_route():
    # for _ in range (n):
    # cities = ['Calgary - YYC', 'Edmonton - YEG', 'Gander - YQX', 'Moncton - YQM', 'Halifax - YHZ', 'Hamilton - YHM', 'London - YXU', 'Montreal - YUL', 'Ottawa - YOW', 'Quebec City - YQB', 'Regina - YQR', 'Saskatoon - YXE', 'St. Johns - YYT', 'Toronto - YYZ', 'Vancouver - YVR', 'Victoria - YYJ', 'Winnipeg - YWG']
    cities = ['Calgary - YYC', 'Edmonton - YEG', 'Halifax - YHZ', 'Montreal - YUL', 'Ottawa - YOW', 'Quebec City - YQB', 'Regina - YQR', 'St. Johns - YYT', 'Toronto - YYZ', 'Vancouver - YVR','Winnipeg - YWG']

    # dep_city = fake.city()
    # arr_city = fake.city()
    perms = permutations (cities, 2)
    for p in perms:
        dep_city = p[0]
        arr_city = p[1]
        Route.objects.create(departure_city = dep_city, arrival_city = arr_city)

def create_trip():
    #NOTE: Error checking is required to make sure that the departure and arrival time is reasonable
    #Setting available dates between April 15 and 30
    sdate = date(2020, 4, 15)   # start date
    edate = date(2020, 4, 30)
    delta = edate - sdate

    dates =[]
    for i in range (delta.days+1):
        day = sdate+timedelta(days=i)
        dates.append(day)

    route_list = [route for route in Route.objects.all()]

    for _ in range(5):
        for route in route_list:
            for trip_date in dates:
                # date = fake.date(pattern='%Y-%m-%d', end_datetime=None)
                # max_trip_date = date(2012, 12, 30)
                # trip_date = fake.date_between(start_date = 'today', end_date = '+1y')
                # trip_date = random.choice(dates)
                arrival_time = fake.time()
                departure_time = fake.time() 
                # route = random.choice(Route.objects.all())
                plane = random.choice(Plane.objects.all())
                Trip.objects.create(date = trip_date, arrival_time = arrival_time, departure_time = departure_time, route_id=route, plane_id=plane)


def create_plane(n=10):
    for _ in range (n):
        company = fake.company()
        model_num = randint(10000,100000)
        max_row = 5
        max_col = 3
        capacity = max_col*max_row
        Plane.objects.create(company = company, model_no = model_num, capacity = capacity, max_row=max_row, max_col=max_col)

# def main():
# create_plane()
# create_route()
# create_passenger()
# create_trip()
    

# if __name__ == '__main__':
#     main()