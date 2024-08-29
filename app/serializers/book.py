"""
 This File will contain books Serializers 

"""
from rest_framework import serializers
from .user import (
    ReadUserSerializer
)
from .review import (
    ReadBookReviewSerializer
)

class ListBookSerializer(serializers.Serializer):
    """ This Serializer will hold data for books list """
    id = serializers.IntegerField()
    title = serializers.CharField()
    published_date = serializers.DateTimeField()


class RetreieveBookSerializer(ListBookSerializer):
    """ This Serializer will hold data for a single book """
    author = ReadUserSerializer()
    content = serializers.CharField()
    summary = serializers.CharField()
    reviews = ReadBookReviewSerializer(source="book_reviews",many=True)