""" This File will contain book apis unit tests """

from rest_framework import status
from django.urls import reverse

from app.serializers import ListBookSerializer, RetreieveBookSerializer

from .base import BaseTest

from app.apis import ListBookAPI, RetrieveBookAPI

from app.models import Book

from datetime import datetime


class BookTestCase(BaseTest):
    """Unit test class for testing Book APIs"""

    def setUp(self):
        super().setUp()

        self.book1 = Book.objects.create(
            title="Test Book 1",
            author=self.user,
            published_date=datetime(2024, 1, 1, 10, 0, 0),
            content="This is the content of Test Book 1.",
            summary="Summary of Test Book 1.",
        )
        self.book2 = Book.objects.create(
            title="Another Test Book",
            author=self.user,
            published_date=datetime(2024, 2, 1, 12, 0, 0),
            content="This is the content of Another Test Book.",
            summary="Summary of Another Test Book.",
        )

        self.list_url = reverse("app:list-books")
        self.retreive_url = reverse("app:retireve-book", args=[self.book1.id])

    def test_url(self):
        """
        def is testing the response for url
        """
        self.validate_sample_url(self.list_url, ListBookAPI)
        self.validate_sample_url(self.retreive_url, RetrieveBookAPI)

    # SUCCESS BOOK LIST TESTS

    def test_list_books_success(self):
        """Test successful Book List"""
        response = self.client.get(self.list_url)
        books = Book.objects.all().order_by("-id")
        serializer = ListBookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("results"), serializer.data)
        self.assertEqual(response.data.get("count"), 2)

    def test_list_books_search(self):
        """Test Successful book list with search"""
        response = self.client.get(self.list_url, {"search": "Test Book 1"})
        books = Book.objects.filter(title__icontains="Test Book 1").order_by("-id")
        serializer = ListBookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 1)
        self.assertEqual(response.data.get("results"), serializer.data)

    def test_list_books_author_filter(self):
        """Test Successful book list with author filter"""
        response = self.client.get(self.list_url, {"author": "testuser"})
        books = Book.objects.filter(author__username="testuser").order_by("-id")
        serializer = ListBookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 2)
        self.assertEqual(response.data.get("results"), serializer.data)

    def test_list_books_published_date_filter(self):
        """Test Successful book list with published_date day_range filter"""
        response = self.client.get(
            self.list_url, {"published_date_day_range": "2024-08-29,2024-08-30"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 0)
        self.assertEqual(response.data.get("results"), [])

    #############################################################################################################

    # FAILED BOOK LIST TESTS

    def test_list_books_unauthenticated(self):
        """Test Book List unauthenticated"""
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ##############################################################################################################

    # SUCCESS RETRIEVE BOOK TESTS

    def test_retrieve_book_success(self):
        """Test Success Retrieve book"""
        response = self.client.get(self.retreive_url)
        book = Book.objects.get(pk=self.book1.id)
        serializer = RetreieveBookSerializer(book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    ##############################################################################################################

    # FAILED RETRIEVE BOOK TESTS

    def test_retrieve_book_not_found(self):
        """Test Failed Not Found Retrieve book"""
        url = reverse("app:retireve-book", kwargs={"pk": 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_book_unauthenticated(self):
        """Test Failed unauthenticated Retrieve book"""
        self.client.logout()
        response = self.client.get(self.retreive_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
