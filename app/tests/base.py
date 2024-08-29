""" This File will hold base class for unit tests """
from rest_framework.test import APITestCase, APIClient
from django.urls import resolve
from importlib import import_module
from app.models import (
    User
)

class BaseTest(APITestCase):
      """ Base Test class for creating a user and authenticate it. """
      def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', email="test@gmail.com", first_name="test", last_name="user")
        self.another_user = User.objects.create_user(username='testuser2', password='testpass', email="test2@gmail.com", first_name="test2", last_name="user")
        self.client.force_authenticate(user=self.user) 

      def validate_url(self, reverse_url, api_class):
            """this function for router validation"""
            func = resolve(reverse_url).func
            module = import_module(func.__module__)
            view = getattr(module, func.__name__)
            self.assertEqual(view, api_class)

      def validate_sample_url(self, reverse_url, api_class):
            """
            this function for path validation
            """
            view = resolve(reverse_url).func.view_class
            self.assertEqual(view, api_class)
