from django.urls import path
from .views import *

urlpatterns = [
    path('main/', MainView.as_view(), name='main'),
    path('search/', SearchResultCreateView.as_view(), name='search'),
    path('filter/', FilterResultCreateView.as_view(), name='filter'),
    path('detail/<int:resume_id>/', ResumeDetailView.as_view()),
]