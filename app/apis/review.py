""" This File will Hold Reviews APIs """

from rest_framework.viewsets import ModelViewSet
from app.serializers import (
    ReviewSerializer,
    ReadBookReviewSerializer
)
from app.models import (
    Review
)
from rest_framework.permissions import IsAuthenticated
from app.permissions import IsReviewOwner

class ReviewAPI(ModelViewSet):
    """ This class will contain Crud APIs for reviews """

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewOwner]
    queryset = Review.objects.all()

    def get_queryset(self):
        return self.queryset.order_by('-id').select_related("book","reviewer")
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadBookReviewSerializer
        return ReviewSerializer