from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', SeniorUserCreate.as_view()),
    path('enterprise/signup/', EnterpriseUserCreate.as_view()),
    path('login/', LoginView.as_view()),
    path('enterprise/login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('<int:id>/', UserView.as_view()),
    path('enterprise/<int:id>/', UserView.as_view()),
    path('profile/<int:id>/', ProfileImageView.as_view()),
    path('secret/<int:id>/', UserSecretView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('check/<str:username>/', CheckDuplicateView.as_view()),
    path('review/list/<int:senior_id>/', GetReviewListView().as_view()),
    path('review/create/', CreateReviewView().as_view()),
    path('review/delete/<int:senior_id>/<int:review_id>/', DeleteReviewView().as_view()),
]

