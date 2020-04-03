from . import models
from rest_framework import serializers

class RouterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Route
        fields = '__all__'


class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plane
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    routes = RouterSerializer(many=True,read_only=True)
    planes = PlaneSerializer(many=True,read_only=True)
    class Meta:
        model = models.Trip
        fields = ['date','arrival_time','departure_time','routes','planes']

class FoodNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Food_Name
        fields = ['food_name']

class PassengerSerializer(serializers.ModelSerializer):
    food = FoodNameSerializer(read_only=True)
    # food_name = serializers.RelatedField(source='food', read_only=True)
    class Meta:
        model = models.Passenger
        fields = ['fname','lname','age','sex','seat_number','food']

