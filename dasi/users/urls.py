from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', SeniorUserCreate.as_view()),
    path('enterprise/signup/', EnterpriseUserCreate.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('enterprise/login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:id>/', UserProfileView.as_view(), name='profile'),
    path('enterprise/<int:id>/', UserProfileView.as_view(), name='enterprise_profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('check/<str:username>/', CheckDuplicateView.as_view(), name='check_duplicate'),
]

