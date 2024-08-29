from django.urls import path
from .apis import (
    RegisterAPI,
    CustomTokenObtainPairView
)

app_name = "app"

urlpatterns = [
    path('auth/register/', RegisterAPI.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
]

