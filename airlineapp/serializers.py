from . import models
from rest_framework import serializers

class TripSerializer(serializers.HyperlinkedModelSerializer):
    # route_details = serializers.RelatedField(source='route_id',read_only=True)
    # plane_details = serializers.RelatedField(source='plane_id',read_only=True)
    # class Meta:
    #     model = models.Trip
    #     fields = ['date','arrival_time','departure_time','route_details','plane_details']
    pass

class FoodNameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Food_Name
        fields = ['food_name']

# class PassengerSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = models.Passenger
#         fields = ['fname','']

class RouterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Route
        fields = '__all__'