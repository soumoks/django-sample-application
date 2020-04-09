from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'gettrips',views.TripViewSet,basename='gettrips')
router.register(r'getfood',views.FoodViewSet)
router.register(r'getroutes',views.RouterViewSet)
router.register(r'getplanes',views.PlaneViewSet)
router.register(r'getfeatures', views.FeatureViewSet)
router.register(r'getfeaturenames', views.FeatureNameViewSet)
router.register(r'getbookings', views.SearchBookingViewSet, basename='getbookings')
# router.register(r'makebooking', views.BookingViewSet.as_view(), basename='makebooking')
# router.register(r'getpassengers/',views.PassengerList.as_view(),basename='getpassengers')

urlpatterns = [
    path('',include(router.urls)),
    path('welcome',views.index,name='index'),
    path('getseats',views.get_total_seats),
    path('getavailseats',views.get_available_seats),
    #Required for post requests. Cannot be part of router.
    path('createfood',views.create_food),
    path('createpassenger',views.create_passenger),
    path('createbooking',views.create_booking),
    path('createbooking/<int:pk>', views.create_booking),
]