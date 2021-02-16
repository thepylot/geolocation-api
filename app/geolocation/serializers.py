from rest_framework import serializers
from core.models import GeoLocation

from .services import get_location

class GeoLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeoLocation
        exclude = ('user', 'id',)
        read_only_fields = ('id', 'user', 'country_name', 'region_code', 'city', 'latitude', 'longitude', 'zip_code',)
    
    def validate_ip(self, ip):
        exists = GeoLocation.objects.filter(ip=ip, user=self.context['request'].user).exists()
        if exists:
            raise serializers.ValidationError('The requested object is already exist')
        return ip
        