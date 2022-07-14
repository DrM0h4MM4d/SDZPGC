from django.urls import path
from .views import (
    ZarinpalSendRequest,
    ZarinPalVerifyView,
)


urlpatterns = [
    path('', ZarinpalSendRequest.as_view(), name='request'),
    path('verify/', ZarinPalVerifyView.as_view(), name='verify'),
]
