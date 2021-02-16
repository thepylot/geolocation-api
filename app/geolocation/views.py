from django.db import IntegrityError

from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from geolocation import serializers
from core.models import GeoLocation
from geolocation.services import get_location

from .exceptions import ExternalApiException


class GeoLocationViewSet(viewsets.ModelViewSet):
    queryset = GeoLocation.objects.all()
    serializer_class = serializers.GeoLocationSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')
    
    def perform_create(self, serializer):
        try:
            data = get_location(serializer.validated_data.get('ip'))
            serializer.save(**data, user=self.request.user)
        except IntegrityError:
            raise ExternalApiException('Some of location data not found for requested IP address or URL') 