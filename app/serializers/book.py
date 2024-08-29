"""
 This File will contain books, reviews Serializers 

"""
from rest_framework import serializers
from app.models import (
    User,
    Book,
    Review
)
from .user import (
    ReadUserSerializer
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