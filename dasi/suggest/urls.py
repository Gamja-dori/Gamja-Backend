from django.urls import path
from .views import *

urlpatterns = [
    path('create/', SuggestCreateView.as_view()),
    path('enterprise/<int:user_id>/', GetSeniorListView.as_view()), 
    path('senior/<int:user_id>/read/', GetReadEnterpriseListView.as_view()), 
    path('senior/<int:user_id>/unread/', GetUnreadEnterpriseListView.as_view()), 
    path('<int:suggest_id>/', GetSuggestDetailView.as_view()),
    path('notifications/<int:user_id>/', NotificationView.as_view()),
    path('notifications/', NotificationView.as_view()),
    path('pay/', PaymentRequestView.as_view()),
    path('pay/approve/', PaymentApproveView.as_view()),
    path('pay/fail/', PaymentFailView.as_view()),
    path('pay/cancel/', PaymentCancelView.as_view()),
    # path('pay/<int:suggest_id>/', GetIsPaidView.as_view()),    
]