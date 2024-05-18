from django.urls import path
from .views import *

urlpatterns = [
    path('create/', SuggestCreateView.as_view(), name='create'),
    path('enterprise/<int:user_id>/', GetSeniorListView.as_view(), name='senior_list'), 
    path('senior/<int:user_id>/', GetEnterpriseListView.as_view(), name='enterprise_list'), 
    path('<int:suggest_id>/', GetSuggestDetailView.as_view(), name='suggest_detail'),
    path('pay/', PaymentRequestView.as_view(), name='payment_request'),
    path('pay/approve/', PaymentApproveView.as_view(), name='payment_approve'),
    path('pay/fail/', PaymentFailView.as_view(), name='payment_fail'),
    path('pay/cancel/', PaymentCancelView.as_view(), name='payment_cancel'),
]

