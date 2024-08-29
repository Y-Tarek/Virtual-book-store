""" This File will contain authentication apis unit tests """
from rest_framework import status
from django.urls import reverse
from .base import (
    BaseTest
)
from app.apis.user import (
    RegisterAPI,
    CustomTokenObtainPairView
)

from app.models import (
    User
)

class AuthTestCase(BaseTest):
    """ Unit test class for testing register/login """
    def setUp(self):
        super().setUp()
        self.register_url = reverse('app:register')
        self.login_url = reverse('app:login')
    
    def test_url(self):
        """
        def is testing the response for url
        """
        self.validate_sample_url(self.register_url, RegisterAPI)
        self.validate_sample_url(self.login_url, CustomTokenObtainPairView)
    
    # SUCCESS REGISTERATION TESTS

    def test_register_success(self):
        """Test successful registration."""
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'Test@12345',
            'confirm_password': 'Test@12345',
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=data['email'])
        self.assertEqual(user.username, data.get('username'))
        self.assertEqual(user.first_name, data.get('first_name'))
        self.assertEqual(user.last_name, data.get('last_name'))
    
    def test_register_username_optional(self):
        """Test registration without a username (optional field)."""
        data = {
            'email': 'test2@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'Test@12345',
            'confirm_password': 'Test@12345',
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=data['email'])
        self.assertEqual(user.email, data.get('email'))
        self.assertIsNone(user.username)
        self.assertEqual(user.first_name, data.get('first_name'))
        self.assertEqual(user.last_name, data.get('last_name'))

    
    # FAILED REGISTERATION TESTS

    def test_register_password_mismatch(self):
        """Test registration fails due to password mismatch."""
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'Test@12345',
            'confirm_password': 'Test@123456',
        }

        response = self.client.post(self.register_url, data, format='json')
    
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertIn("Password fields didn't match.", response.data['password'])


    def test_register_email_already_exists(self):
        """Test registration fails if email is already in use."""
        User.objects.create_user(
            username='existinguser',
            email='test@example.com',
            password='Existing@12345'
        )

        data = {
            'email': 'test@example.com',
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'New@12345',
            'confirm_password': 'New@12345',
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn('This field must be unique.', response.data['email'])
    
################################################################################################

# SUCCESS LOGIN TESTS

    def test_login_success(self):
        """Test successful login."""
        
        # Using another_user credintials defined in base
        data = {
            'email': 'test2@gmail.com',
            'password': 'testpass',
        }

        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

# FAILED LOGIN TESTS

    def test_login_failure_invalid_password(self):
        """Test login fails with incorrect password."""
        data = {
            'email': 'test@example.com',
            'password': 'WrongPassword',
        }

        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')

    def test_login_failure_nonexistent_user(self):
        """Test login fails with a non-existent user."""
        data = {
            'email': 'nonexistent@example.com',
            'password': 'SomePassword',
        }

        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')