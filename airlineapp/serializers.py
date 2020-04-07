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
        # fields = 'food_name'

class PassengerSerializer(serializers.ModelSerializer):
    #use the same name as that of the column name in Food_Name
    # food_name = FoodNameSerializer(read_only=True)
    class Meta:
        model = models.Passenger
        fields = ['fname','lname','age','sex','seat_number','food_name']
        # fields = '__all__'
    def create(self, validated_data):
        print(f"Validated data: {validated_data}")
        fname = validated_data.pop('fname')
        lname = validated_data.pop('lname')
        age = validated_data.pop('age')
        sex = validated_data.pop('sex')
        seat_number = validated_data.pop('seat_number')
        f = validated_data.pop('food_name')
        # print(f"food name present in validated data: {food_name_id}")
        # f = models.Food_Name.objects.get(id=food_name)
        # print(f"selected food object: {food_name}")
        p = models.Passenger.objects.create(fname=fname,lname=lname,age=age,sex=sex,seat_number=seat_number,food_name=f)
        return p
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
    # trip_id = TripSerializer()
    # passenger_id = PassengerSerializer(read_only=True)

    class Meta:
        model = models.Booking
        fields = '__all__'
        # fields = ['book_type','trip_id','passenger_id']

        # def create(self, validated_data):
        #     print(f"Validated data: {validated_data}")
        #     book_type = validated.pop('book_type')

        #     trip_data = validated_data.pop('trip_id')
        #     print(f"Trip data: {trip_data}")

        #     #this field should contain the entire details for passenger
        #     passenger_data = validated_data.pop('passenger_id')
        #     print(f"Pasenger data: {passenger_data}")

            #create passenger in booking as this is a new passenger object
            # p = models.Passenger.objects.create(**passenger_data)
            # print(f"Created passenger is: {p}")
            # b = model.Booking.objects.create(book_type=book_type,trip_id=trip_data,passenger_id=p)
            # return b
