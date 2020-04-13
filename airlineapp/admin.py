from django.contrib import admin
from .models import Trip,Route,Plane,Food_Name,Feature,Passenger,Booking,Feature_Name,Booking_Type
from airlineapp.services import get_passengers, send_notification
# Register your models here.

def notify_passengers_trip_delete(modeladmin,request,queryset):
    """
    Notify passengers who have chosen a particular trip that the trip has been cancelled
    We do this by obtaining the trip_id that needs to be deleted by iterating over
    the queryset object,call get_passengers to return the 
    list of passengers
    """
    print("Notifying passengers of a Trip cancellation")    
    passengers_list = []
    for trip in queryset:
        passengers_list.append(get_passengers(trip.id))
    
    print("List of passengers")
    print(passengers_list)
    #call services.send_notification with passenger email ids here
    #passengers_list is a list of lists. Each list contains the passenger IDs for each trip
    for plist in passengers_list:
        for p in plist:
            send_notification(p,"cancel")
    print("Deleting selected trip/s. This action will delete any bookings with this trip ID as well")
    #reference: https://docs.djangoproject.com/en/3.0/topics/db/queries/
    queryset.delete()

#required to provide a better description on the admin console
notify_passengers_trip_delete.short_description = "Delete Trip and notify passengers"


class Trip_Admin(admin.ModelAdmin):
    list_display = ['id','date','arrival_time','departure_time','route_id','plane_id']
    ordering = ['id']
    actions = [notify_passengers_trip_delete]

"""Adding the following custom admin classes for a better display on the admin console"""
class Booking_Admin(admin.ModelAdmin):
    list_display = ['id','book_type','trip_id','passenger_id']
    ordering = ['id']

class Booking_Type_Admin(admin.ModelAdmin):
    list_display = ['id','booking_id','trip_id','passenger_id']
    ordering = ['id']

class Passenger_Admin(admin.ModelAdmin):
    list_display = ['id','fname','lname','email','age','sex','seat_number','food_name']
    ordering = ['id']

class Route_Admin(admin.ModelAdmin):
    list_display = ['id','departure_city','arrival_city']
    ordering = ['id']

class Plane_Admin(admin.ModelAdmin):
    list_display = ['id','model_no','company','max_row','max_col']
    ordering = ['id']

class Food_Name_Admin(admin.ModelAdmin):
    list_display = ['id','food_name']
    ordering = ['id']

class Feature_Admin(admin.ModelAdmin):
    list_display = ['id','feature_desc']
    ordering = ['id']

class Feature_Name_Admin(admin.ModelAdmin):
    list_display = ['id','plane_id','feature_id']
    ordering = ['id']


admin.site.register(Trip,Trip_Admin)
admin.site.register(Route,Route_Admin)
admin.site.register(Plane,Plane_Admin)
admin.site.register(Food_Name,Food_Name_Admin)
# admin.site.register(Feature,Feature_Admin)
admin.site.register(Passenger,Passenger_Admin)
admin.site.register(Booking,Booking_Admin)
# admin.site.register(Feature_Name,Feature_Name_Admin)
# admin.site.register(Booking_Type,Booking_Type_Admin)