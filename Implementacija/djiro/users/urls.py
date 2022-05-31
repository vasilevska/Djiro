from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *

urlpatterns = [
    path('sample/', SampleView.as_view()),
    path('api-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', registration_view, name="registration")
]
