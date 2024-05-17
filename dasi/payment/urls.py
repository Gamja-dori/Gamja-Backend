from django.urls import path
from .views import *

urlpatterns = [
    path('', PaymentRequestView.as_view(), name='paymentRequst'),
    path('approve/', ApproveView.as_view(), name='approve'),
    path('fail/', FailView.as_view(), name='fail'),
    path('cancel/', CancelView.as_view(), name='cancel'),
]