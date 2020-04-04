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
from datetime import date

fake = Faker()

def create_passenger(n=100):
    sex_type = ['M','F']
    for _ in range (n):
        name = fake.name()
        fname = name.split()[0]
        lname = name.split()[1]
        age = randint(1,100)
        sex = random.choice(sex_type)
        seat_list = [random.choice(string.ascii_uppercase),random.choice(string.digits)]
        seat_num = "".join(seat_list)
        food_num = random.choice(Food_Name.objects.all())
        Passenger.objects.create(fname = fname, lname = lname, age = age, sex = sex, seat_number = seat_num, food_name = food_num)
        
def create_route():
    # for _ in range (n):
    cities = ['Calgary - YYC', 'Edmonton - YEG', 'Gander - YQX', 'Moncton - YQM', 'Halifax - YHZ', 'Hamilton - YHM', 'London - YXU', 'Montreal - YUL', 'Ottawa - YOW', 'Quebec City - YQB', 'Regina - YQR', 'Saskatoon - YXE', 'St. Johns - YYT', 'Toronto - YYZ', 'Vancouver - YVR', 'Victoria - YYJ', 'Winnipeg - YWG']
    # dep_city = fake.city()
    # arr_city = fake.city()
    perms = permutations (cities, 2)
    for p in perms:
        dep_city = p[0]
        arr_city = p[1]
        Route.objects.create(departure_city = dep_city, arrival_city = arr_city)

def create_trip(n=100):
    #NOTE: Error checking is required to make sure that the departure and arrival time is reasonable
    for _ in range (n):
        # date = fake.date(pattern='%Y-%m-%d', end_datetime=None)
        # max_trip_date = date(2012, 12, 30)
        trip_date = fake.date_between(start_date = 'today', end_date = '+1y')
        arrival_time = fake.time()
        departure_time = fake.time() 
        route = random.choice(Route.objects.all())
        # r_id = route.id
        plane = random.choice(Plane.objects.all())
        # p_id = plane.id
        Trip.objects.create(date = trip_date, arrival_time = arrival_time, departure_time = departure_time, route_id=route, plane_id=plane)


def create_plane(n=20):
    for _ in range (n):
        company = fake.company()
        model_num = randint(10000,100000)
        capacity = randint(100,300)
        max_row = randint(20,40)
        max_col = randint(3, 10)
        Plane.objects.create(company = company, model_no = model_num, capacity = capacity, max_row=max_row, max_col=max_col)

# def main():
create_passenger(100)
create_plane(20)
create_route()
create_trip()
    

# if __name__ == '__main__':
#     main()