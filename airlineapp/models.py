from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

"""
Some things to note about how Django creates primary key and foreign keys.
By default, Django adds a primary key(integer field) with the name of class as follows
for a class Question, it will use question_id as primary key.
This setting can be overridden by explicity mentioning the primary key while defining the field.
For example,
name = models.CharField(max_length=100, primary_key=True)

A few notes regarding the foreign key,
class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)

This line creates a question_id in the Choice table. 
So basically, Django uses the primary key of Question table to create a foreign key in the choice table

Model documentation
https://docs.djangoproject.com/en/3.0/ref/models/fields/

Useful fields.
CharField
DateField
DateTimeField
IntegerField
DurationField
EmailField
FloatField
ImageField

By default, Django gives each model the following field:

id = models.AutoField(primary_key=True)

We can try returning the id in each to string method by returning
self.id
"""
# Create your models here.
#Foreign key usage reference:
#https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_one/
class Route(models.Model):
    """
    Contains the available routes. 
    For example : Calgary to Vancouver
    """
    departure_city = models.CharField(max_length=30,default=None)
    arrival_city = models.CharField(max_length=30,default=None)

    def __str__(self):
        return f"Departure: {self.departure_city} | Arrival: {self.arrival_city}"

class Plane(models.Model):
    """
    Contains information about each plane
    """
    company = models.CharField(max_length=100,default=None)
    model_no = models.PositiveIntegerField(default=None)
    capacity = models.PositiveIntegerField(default=None)
    max_row = models.PositiveIntegerField(default=None)
    max_col = models.PositiveIntegerField(default=None)

    def __str__(self):
        return f"Plane ID: {self.id} is {self.company} {self.model_no}"


class Trip(models.Model):
    date = models.DateField(default=None)
    arrival_time = models.TimeField(default=None)
    departure_time = models.TimeField(default=None)
    route_id = models.ForeignKey(Route,on_delete=models.CASCADE,default=None,related_name='routes')
    plane_id = models.ForeignKey(Plane,on_delete=models.CASCADE,default=None,related_name='planes')

    def __str__(self):
        my_str = f"Date: {self.date}, Arrival Time: {self.arrival_time}, Departure Time: {self.departure_time}, Route ID: {self.route_id}, Plane ID: {self.plane_id}"
        return my_str


class Food_Name(models.Model):
    """
    Lookup table for food name
    """
    food_name = models.CharField(max_length=30)
    # passenger = models.ForeignKey(Passenger,on_delete=models.CASCADE,related_name='passenger',default=None)

    def __str__(self):
        return self.food_name


class Passenger(models.Model):

    SEX_TYPE = [
        ('M', 'M'),
        ('F', 'F')
    ]

    """
    Passenger information
    """
    fname = models.CharField(max_length=30,default=None)
    lname = models.CharField(max_length=30,default=None)
    age = models.IntegerField(validators=[MinValueValidator(0, 'Please enter correct value'), MaxValueValidator(100, 'Please enter correct value')],default=None)
    sex = models.CharField(max_length=1, choices = SEX_TYPE,default='M')
    seat_number = models.CharField(max_length=4,default=None)
    food_name = models.ForeignKey(Food_Name,on_delete=models.CASCADE,default=None,related_name='food')

    def __str__(self):
        """return individual passenger information
        """
        return f"Name: {self.fname} {self.lname}, Seat: {self.seat_number}, Food Pref: {self.food_name}"
        # return f"Name: {self.fname} {self.lname}, Seat: {self.seat_number}"
        

class Booking(models.Model):
    BOOKING_TYPE = [
        ("One-Way","One-Way"),
        ("Round-Trip","Round-Trip")
    ]
    book_type = models.CharField(max_length=10,choices=BOOKING_TYPE,default="One-Way")
    trip_id = models.ForeignKey(Trip,on_delete=models.CASCADE,default=None)
    passenger_id = models.ForeignKey(Passenger,on_delete=models.CASCADE,default=None)

    def __str__(self):
        my_str = f"Passenger with ID: {self.passenger_id} has Trip ID: {self.trip_id} and Type is {self.book_type}"
        return my_str


#TODO: Need to check the requirement for this table
class Booking_Type(models.Model):
    booking_id = models.ForeignKey(Booking,on_delete=models.CASCADE,default=None)
    trip_id = models.ForeignKey(Trip,on_delete=models.CASCADE,default=None)
    passenger_id = models.ForeignKey(Passenger,on_delete=models.CASCADE,default=None)

    def __str__(self):
        my_str = f"Booking ID: {self.booking_id}, Trip ID: {self.trip_id}, Passenger ID: {self.passenger_id}"
        return my_str



class Feature(models.Model):
    """
    Contains the description of each feature
    """
    feature_desc = models.CharField(max_length=200,default=None)

    def __str__(self):
        return self.feature_desc

class Feature_Name(models.Model):
    """
    This table is required to tie together the Plane with the different features.
    This table was created to avoid multivalues in Plane.
    Each plane can have multiple features part of the "Feature" Table
    This table will contain two foreign keys i.e planeID and feature_ID
    """
    plane_id = models.ForeignKey(Plane,on_delete=models.CASCADE,default=None)
    feature_id = models.ForeignKey(Feature,on_delete=models.CASCADE,default=None)

    def __str__(self):
        my_str = f"Plane ID:{self.plane_id} has feature ID:{self.feature_id}";
        return my_str
