from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

import requests
from rest_framework import status
from rest_framework.test import APIClient

from core.models import GeoLocation
from geolocation.serializers import GeoLocationSerializer
from geolocation.services import get_location

LOCATIONS_URL = reverse('geolocation:location-list')

def find_current_ip():
    return requests.get('http://ipgrab.io').text

def sample_mocked_geolocation(**params):
    """Create and return a sample mocked geolocation object"""
    mock_data = {
        'ip': '10.0.0.1',
        'country_name':'Mars',
        'region_code':'SOL512',
        'city': 'RedSand',
        'latitude':49.02342,
        'longitude':40.34342,
        'zip':'1052'
    }
    mock_data.update(params)

    return mock_data

def sample_geolocation(user, **params):
    """Create and return a sample geolocation object"""
    defaults = {
        'ip': '10.0.0.1',
        'country_name':'Mars',
        'region_code':'SOL512',
        'city': 'RedSand',
        'latitude':49.02342,
        'longitude':40.34342,
        'zip_code':'1052'
    }
    defaults.update(params)

    return GeoLocation.objects.create(user=user, **defaults)

def detail_url(geolocation_id):
    return reverse('geolocation:location-detail', args=[geolocation_id])

class PublicGeoLocationApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
       
    def test_auth_required(self):
        """Test that auth is required"""
        res = self.client.get(LOCATIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateGeoLocationApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email='test@email.com',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retiriving a list of locations"""
        sample_geolocation(user=self.user)
        sample_geolocation(user=self.user)

        res = self.client.get(LOCATIONS_URL)

        geolocation = GeoLocation.objects.all().order_by('-id')
        serializer = GeoLocationSerializer(geolocation, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_geolocation_limited_to_user(self):
            """Test retrieving geolocation for user"""
            user2 = get_user_model().objects.create_user(
                'test@gmail.com',
                'testpass'
            )
            sample_geolocation(user=user2)
            sample_geolocation(user=self.user)

            res = self.client.get(LOCATIONS_URL)

            geolocation = GeoLocation.objects.filter(user=self.user).order_by('-id')
            serializer = GeoLocationSerializer(geolocation, many=True)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(len(res.data), 1)
            self.assertEqual(res.data, serializer.data)

    @patch('requests.get')
    def test_create_geolocation_successful(self, mock_request):
        """Test geolocation created successful"""
        mock_request.return_value.json.return_value = sample_mocked_geolocation()
        payload = {'ip': mock_request.return_value.json.return_value['ip']}
        res = self.client.post(LOCATIONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['ip'], payload['ip'])

    @patch('requests.get')
    def test_create_geolocation_with_invalid_response(self, mock_request):
        """Test geolocation creation failed with invalid response data"""
        mock_request.return_value.json.return_value = sample_mocked_geolocation(city=None)
        payload = {'ip': mock_request.return_value.json.return_value['ip']}
        res = self.client.post(LOCATIONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch('requests.get')
    def test_create_unique_geolocation_for_user(self, mock_request):
            """Test creating unique geolocation object for a particular user"""
            for i in range (2):
                mock_request.return_value.json.return_value = sample_mocked_geolocation()
                payload = {'ip':  mock_request.return_value.json.return_value['ip']}

                res = self.client.post(LOCATIONS_URL, payload)

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_geolocation(self):
            """Test delete geoloation object"""
            geolocation_obj = sample_geolocation(user=self.user)
            url = detail_url(geolocation_obj.id)

            self.client.delete(url)  
            res = self.client.get(url)

            self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    