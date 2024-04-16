from django.urls import path
from .views import *

urlpatterns = [
    path('main/', MainView.as_view(), name='main'),
    path('search/', SearchView.as_view(), name='search'),
    path('filter/', SearchView.as_view(), name='filter'),
    path('detail/<int:resume_id>/', ResumeDetailView.as_view()),
]