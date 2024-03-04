from django.urls import path
from .views import MyTokenObtainPairView, SeniorUserCreate, EnterpriseUserCreate
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SeniorUserCreate.as_view()),
    path('enterprise/signup/', EnterpriseUserCreate.as_view()),
    path('token/',  MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

