from django.contrib import admin
from .models import Trip,Route,Plane,Food_Name,Feature,Passenger,Booking,Feature_Name,Booking_Type
# Register your models here.

admin.site.register(Trip)
admin.site.register(Route)
admin.site.register(Plane)
admin.site.register(Food_Name)
admin.site.register(Feature)
admin.site.register(Passenger)
admin.site.register(Booking)
# admin.site.register(Feature_Name)
admin.site.register(Booking_Type)