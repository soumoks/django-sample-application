from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'gettrips',views.TripViewSet)
router.register(r'getfood',views.FoodViewSet)
router.register(r'getroutes',views.RouterViewSet)


urlpatterns = [
    path('',include(router.urls)),
    path('',views.index,name='index'),
]