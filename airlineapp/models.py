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
class Route(models.Model):
    """
    Contains the available routes. 
    For example : Calgary to Vancouver
    """
    departure_city = models.CharField(max_length=30)
    arrival_city = models.CharField(max_length=30)

    def __str__(self):
        return f"Departure: {self.departure_city} | Arrival: {self.arrival_city}"

class Plane(models.Model):
    """
    Contains information about each plane
    """
    company = models.CharField(max_length=100)
    model_no = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    max_row = models.PositiveIntegerField()
    max_col = models.PositiveIntegerField()

    def __str__(self):
        return f"plane with ID:{self.id} has max_row: {self.max_row} and max_col: {self.max_col}"


class Trip(models.Model):
    date = models.DateField()
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    route_id = models.ForeignKey(Route,on_delete=models.CASCADE)
    plane_id = models.ForeignKey(Plane,on_delete=models.CASCADE)

    def __str__(self):
        my_str = f"Date: {self.date}, Arrival Time: {self.arrival_time}, Departure Time: {self.departure_time}, Route ID: {self.route_id}, Plane ID: {self.plane_id}"
        return my_str


class Food_Name(models.Model):
    """
    Lookup table for food name
    """
    food_name = models.CharField(max_length=30)
    # passenger = models.ForeignKey(Passenger,on_delete=models.CASCADE)

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
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    age = models.IntegerField(validators=[MinValueValidator(0, 'Please enter correct value'), MaxValueValidator(100, 'Please enter correct value')])
    sex = models.CharField(max_length=1, choices = SEX_TYPE)
    seat_number = models.CharField(max_length=4)
    food_name = models.ForeignKey(Food_Name,on_delete=models.CASCADE)

    def __str__(self):
        """return individual passenger information
        """
        return f"Name: {self.fname} {self.lname}, Seat: {self.seat_number}, Food Pref: {self.food_name}"



class Booking(models.Model):
    BOOKING_TYPE = [
        ("One-Way","One-Way"),
        ("Round-Trip","Round-Trip")
    ]
    book_type = models.CharField(max_length=10,choices=BOOKING_TYPE)
    trip_id = models.ForeignKey(Trip,on_delete=models.CASCADE)
    passenger_id = models.ForeignKey(Passenger,on_delete=models.CASCADE)



class Booking_Type(models.Model):
    pass






class Feature(models.Model):
    """
    Contains the description of each feature
    """
    feature_desc = models.CharField(max_length=200)

    def __str__(self):
        return self.feature_desc

class Feature_Name(models.Model):
    """
    This table is required to tie together the Plane with the different features.
    This table was created to avoid multivalues in Plane.
    Each plane can have multiple features part of the "Feature" Table
    This table will contain two foreign keys i.e planeID and feature_ID
    """
    plane_id = models.ForeignKey(Plane,on_delete=models.CASCADE)
    feature_id = models.ForeignKey(Feature,on_delete=models.CASCADE)

    def __str__(self):
        my_str = f"Plane ID:{self.plane_id} has feature ID:{self.feature_id}";
        return my_str
