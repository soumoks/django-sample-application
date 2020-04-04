from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'gettrips',views.TripViewSet,basename='gettrips')
router.register(r'getfood',views.FoodViewSet)
router.register(r'getroutes',views.RouterViewSet)
router.register(r'getplanes',views.PlaneViewSet)
# router.register(r'getpassengers/',views.PassengerList.as_view(),basename='getpassengers')

urlpatterns = [
    path('',include(router.urls)),
    path('welcome',views.index,name='index'),
]