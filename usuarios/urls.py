from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegistroView

urlpatterns = [
    path('auth/register/', RegistroView.as_view(), name='registro'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]