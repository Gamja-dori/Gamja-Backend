from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreateSuggestView.as_view()),
    path('enterprise/<int:user_id>/', GetSeniorListView.as_view()), 
    path('enterprise/completed/<int:user_id>/', GetCompletedSeniorListView.as_view()), 
    path('enterprise/in-progress/<int:user_id>/', GetInProgressSeniorListView.as_view()), 
    path('notifications/enterprise/<int:user_id>/', GetEnterpriseNotificationsView.as_view()), 
    path('notifications/senior/<int:user_id>/', GetSeniorNotificationsView.as_view()), 
    path('notifications/count/<int:user_id>/', GetNotificationCountView.as_view()),
    path('notifications/', PatchNotificationView.as_view()),
    path('<int:suggest_id>/', GetSuggestDetailView.as_view()),
    path('progress/<int:suggest_id>/', GetProgressView.as_view()),
    path('progress/update/', UpdateProgressView.as_view()),
    path('pay/', PaymentRequestView.as_view()),
    path('pay/approve/<int:payment_id>/<str:pg_token>/', PaymentApproveView.as_view()),
    path('pay/<int:suggest_id>/', GetIsPaidView.as_view()),    
]