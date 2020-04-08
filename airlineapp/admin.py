from django.contrib import admin
from .models import Trip,Route,Plane,Food_Name,Feature,Passenger,Booking,Feature_Name,Booking_Type
from airlineapp.services import get_passengers
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
    print("Deleting selected trip/s. This action will delete any bookings with this trip ID as well")
    #reference: https://docs.djangoproject.com/en/3.0/topics/db/queries/
    queryset.delete()

#required to provide a better description on the admin console
notify_passengers_trip_delete.short_description = "Delete Trip and notify passengers"


class Trip_Admin(admin.ModelAdmin):
    list_display = ['id','date','arrival_time','departure_time','route_id','plane_id']
    ordering = ['id']
    actions = [notify_passengers_trip_delete]



admin.site.register(Trip,Trip_Admin)
admin.site.register(Route)
admin.site.register(Plane)
admin.site.register(Food_Name)
admin.site.register(Feature)
admin.site.register(Passenger)
admin.site.register(Booking)
admin.site.register(Feature_Name)
admin.site.register(Booking_Type)