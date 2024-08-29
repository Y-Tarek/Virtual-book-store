""" This File will Hold Books & Reviews APIs """

from rest_framework.generics import (
  ListAPIView,
  RetrieveAPIView
)
from app.models import (
    Book,
    Review
)
from app.serializers import (
    ListBookSerializer,
    RetreieveBookSerializer
)
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from app.filters import BookFilter

class ListBookAPI(ListAPIView):
    """ List Available books API """
    serializer_class = ListBookSerializer
    queryset = Book.objects.all().order_by('-id')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = BookFilter
    search_fields = ['title']


class RetrieveBookAPI(RetrieveAPIView):
    """ Retrieve a single book API """
    serializer_class = RetreieveBookSerializer
    queryset = Book.objects.select_related("author")
    permission_classes = [IsAuthenticated]