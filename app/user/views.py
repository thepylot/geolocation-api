from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings
from user.serializers import UserSeralizer

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSeralizer

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the auth user"""
    serializer_class = UserSeralizer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        """Retrieve and return auth user"""
        return self.request.user