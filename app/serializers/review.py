"""
 This File will contain review Serializers 

"""
from rest_framework import serializers
from app.serializers import (
    ReadUserSerializer
)
from app.models import (
    Review
)
from rest_framework.validators import UniqueTogetherValidator

class ReviewSerializer(serializers.ModelSerializer):
    """ This Serializer will handle Review data """
    reviewer = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        """ Meta data for review serializer """
        model = Review
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['book', 'reviewer'],
                message="This Book is already reviewd by this user."
            )
        ]
    
    def validate_rating(self,rating):
        """ Validate rating value not to exceed 5 to be only from 1 to 5. """
        if rating > 5:
            raise serializers.ValidationError(
                "rating can't be more than 5"
            )
        return rating

class ReadBookReviewSerializer(serializers.Serializer):
    """ This Serializer will be readonly for reading reviews """

    id  = serializers.IntegerField()
    review_text = serializers.CharField()
    rating = serializers.IntegerField()
    reviewer = ReadUserSerializer()

