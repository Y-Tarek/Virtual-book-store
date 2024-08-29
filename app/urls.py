from django.urls import path, include
from .apis import (
    RegisterAPI,
    CustomTokenObtainPairView,
    ListBookAPI,
    RetrieveBookAPI,
    ReviewAPI
)
from rest_framework import routers

app_name = "app"

router = routers.SimpleRouter()
router.register("review", ReviewAPI, basename="review-apis")

urlpatterns = [
    path("", include(router.urls)),
    path('auth/register/', RegisterAPI.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('book/', ListBookAPI.as_view(), name='list-books'),
    path('book/<int:pk>/', RetrieveBookAPI.as_view(), name='retireve-book'),
]

