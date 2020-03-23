from django.db import models
from django.utils import timezone

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
class Trip(models.Model):
    pass

class Booking(models.Model):
    pass

class Plane(models.Model):
    """
    Contains information about each plane
    """
    company = models.CharField(max_length=100)
    model_no = models.IntegerField()
    capacity = models.IntegerField()
    max_row = models.IntegerField()
    max_col = models.IntegerField()

    def __str__(self):
        return f"plane with ID:{self.id} has max_row: {self.max_row} and max_col: {self.max_col}"

class Booking_Type(models.Model):
    pass

class Route(models.Model):
    """
    Contains the available routes. 
    For example : Calgary to Vancouver
    """
    departure_city = models.CharField(max_length=30)
    arrival_city = models.CharField(max_length=30)

    def __str__(self):
        return f"Departure: {self.departure_city} | Arrival: {self.arrival_city}"

class Food_Name(models.Model):
    """
    Lookup table for food name
    """
    food_name = models.CharField(max_length=30)

    def __str__(self):
        return self.food_name

class Passenger(models.Model):
    """
    Passenger information
    """
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    seat_number = models.CharField(max_length=4)
    food_name = models.ForeignKey(Food_Name,on_delete=models.CASCADE)

    def __str__(self):
        """return individual passenger information
        """
        return f"Name: {self.fname} {self.lname}, Seat: {self.seat_number}, Food Pref: {self.food_name}"


class Feature(models.Model):
    """
    Contains the description of each feature
    """
    feature_desc = models.CharField(max_length=200)

    def __str__(self):
        return self.feature_desc

class Feature_Name(models.Model):
    pass


