from django.urls import path
from .apis import (
    RegisterAPI,
    CustomTokenObtainPairView,
    ListBookAPI,
    RetrieveBookAPI
)

app_name = "app"

urlpatterns = [
    path('auth/register/', RegisterAPI.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('book/', ListBookAPI.as_view(), name='list-books'),
    path('book/<int:pk>/', RetrieveBookAPI.as_view(), name='retireve-book'),
]

