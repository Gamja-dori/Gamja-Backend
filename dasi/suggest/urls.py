from django.urls import path
from .views import *

urlpatterns = [
    path('pay/', PaymentRequestView.as_view(), name='paymentRequest'),
    path('pay/approve/', ApproveView.as_view(), name='approve'),
    path('pay/fail/', FailView.as_view(), name='fail'),
    path('pay/cancel/', CancelView.as_view(), name='cancel'),
]

