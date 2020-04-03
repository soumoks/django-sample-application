from . import models
from rest_framework import serializers

class RouterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Route
        fields = ['departure_city','arrival_city']


class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plane
        fields = ['company','model_no','capacity','max_row','max_col']

class TripSerializer(serializers.ModelSerializer):
    #use the same name as that of the column name in Trip
    route_id = RouterSerializer(read_only=True)
    plane_id = PlaneSerializer(read_only=True)
    class Meta:
        model = models.Trip
        fields = ['date','arrival_time','departure_time','route_id','plane_id']

class FoodNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Food_Name
        fields = ['food_name']

class PassengerSerializer(serializers.ModelSerializer):
    #use the same name as that of the column name in Food_Name
    food_name = FoodNameSerializer(read_only=True)
    class Meta:
        model = models.Passenger
        fields = ['fname','lname','age','sex','seat_number','food_name']

