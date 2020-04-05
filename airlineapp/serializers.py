from . import models
from rest_framework import serializers

#https://www.django-rest-framework.org/api-guide/relations/
class RouterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Route
        # fields = ['departure_city','arrival_city']
        fields = '__all__'


class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plane
        # fields = ['company','model_no','capacity','max_row','max_col']
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    #use the same name as that of the column name in Trip
    route_id = RouterSerializer(read_only=True)
    plane_id = PlaneSerializer(read_only=True)
    class Meta:
        model = models.Trip
        # fields = ['date','arrival_time','departure_time','route_id','plane_id']
        fields = '__all__'

class FoodNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Food_Name
        fields = '__all__'

class PassengerSerializer(serializers.ModelSerializer):
    #use the same name as that of the column name in Food_Name
    food_name = FoodNameSerializer(read_only=True)
    class Meta:
        model = models.Passenger
        # fields = ['fname','lname','age','sex','seat_number','food_name']
        fields = '__all__'

class FeatureSerializer(serializers.ModelSerializer):  
    class Meta:
        model = models.Feature
        fields = '__all__'

class FeatureNameSerializer(serializers.ModelSerializer):
    #use the same name as that of the column name in Trip
    feature_id = FeatureSerializer(read_only=True)
    plane_id = PlaneSerializer(read_only=True)
    class Meta:
        model = models.Feature_Name
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    trip_id = TripSerializer()
    passenger_id = PassengerSerializer()

    class Meta:
        model = models.Booking
        fields = '__all__'

    # def create(self, validated_data):
    #     trip_data = validated_data.pop('trip_id')
    #     passenger_data = validated_data.pop('passenger_id')

    #     trips = models.Trip.objects.create(**validated_data)
    #     passengers = models.Passenger.objects.create(**validated_data)
    #     return (trips, passengers)
