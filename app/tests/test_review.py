""" This File will contain Review apis unit tests """

from rest_framework import status
from django.urls import reverse

from app.models import Review, Book
from .base import BaseTest
from app.apis import ReviewAPI
from datetime import datetime

class ReviewTestCase(BaseTest):
    """Unit test class for testing Review APIs"""

    def setUp(self):
        super().setUp()

        self.book = Book.objects.create(
            title="Another Test Book",
            author=self.user,
            published_date=datetime(2024, 2, 1, 12, 0, 0),
            content="This is the content of Another Test Book.",
            summary="Summary of Another Test Book.",
        )

        self.review = Review.objects.create(
            book=self.book,
            reviewer=self.user,
            review_text="This is a test review.",
            rating=5
        )
        self.review_url = reverse("app:review-apis-list")
        self.review_detail_url = reverse("app:review-apis-detail",args=[self.review.id])
    
    def test_url(self):
        """
         def is testing the response for url
        """
        self.validate_url(self.review_url, ReviewAPI)
        self.validate_url(self.review_detail_url, ReviewAPI)
    
    # SUCCESS REVIEW TESTS

    def test_create_review_success(self):
        """ Test Success review creation """
        data = {
            'book': self.book.id,
            'review_text': 'New test review.',
            'rating': 4
        }
        self.client.force_authenticate(user=self.another_user)
        response = self.client.post(self.review_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
    
    def test_update_review_success(self):
        "Test Success review Update "
        data = {
            "rating":3
        }
        response = self.client.patch(self.review_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 3)
    
    def test_delete_review_success(self):
        "Test Success review delete "
        response = self.client.delete(self.review_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    
    #########################################################################
    
     # FAILED REVIEW TESTS

    def test_create_review_failed_uniqie_together(self):
        """ Test failed review creation  with unique together validation"""
        data = {
            'book': self.book.id,
            'review_text': 'New test review.',
            'rating': 4
        }
        response = self.client.post(self.review_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This Book is already reviewd by this user.", response.data['non_field_errors'])

    def test_create_review_failed_invalid_rating(self):
        """ Test failed review creation invalid rating value"""
        data = {
            'book': self.book.id,
            'review_text': 'New test review.',
            'rating': 8
        }
        self.client.force_authenticate(user=self.another_user)
        response = self.client.post(self.review_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("rating can't be more than 5", response.data['rating'])
    
    def test_create_review_failed_invalid_data(self):
        """ Test failed review creation invalid data"""
        data = {
            'book': '',
            'review_text': 'New test review.',
            'rating': 4
        }
        self.client.force_authenticate(user=self.another_user)
        response = self.client.post(self.review_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field may not be null.", response.data['book'])
    
    def test_create_review_failed_no_data(self):
        """ Test failed review creation no data"""
        data = {}
        self.client.force_authenticate(user=self.another_user)
        response = self.client.post(self.review_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", response.data['book'])
        self.assertIn("This field is required.", response.data['rating'])
        self.assertIn("This field is required.", response.data['review_text'])
    
    def test_update_review_failed_not_owner(self):
        "Test Failed review Update as authenticated user not the reviewer"
        data = {
            "rating":2
        }
        self.client.force_authenticate(user=self.another_user)
        response = self.client.patch(self.review_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_review_failed_invalid_data_rating(self):
        "Test Failed review Update as data are invalid with rating value"
        data = {
            "rating":''
        }
        response = self.client.patch(self.review_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A valid integer is required.", response.data['rating'])
    
    def test_update_review_failed_invalid_data_book_no_exist(self):
        "Test Failed review Update as data are invalid with doesn't exist book pk"
        data = {
            "book":99
        }
        response = self.client.patch(self.review_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid pk \"99\" - object does not exist.", response.data['book'])
    
    def test_delete_review_failed(self):
        "Test failed review delete "
        self.client.force_authenticate(user=self.another_user)
        response = self.client.delete(self.review_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_review_failed_not_found(self):
        "Test failed review delete as review not found "
        url = reverse("app:review-apis-detail",args=[50])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)