""" This File will Hold User APIs """

from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from app.serializers import RegisterSerializer
from app.models import User


class RegisterAPI(CreateAPIView):
    """Register API"""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """Login API"""
