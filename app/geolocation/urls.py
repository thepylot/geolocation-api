from django.urls import path, include
from rest_framework.routers import DefaultRouter

from geolocation import views

router = DefaultRouter()
router.register('locations', views.GeoLocationViewSet, basename='location')

app_name = 'geolocation'

urlpatterns = [
    path('', include(router.urls))
    ]