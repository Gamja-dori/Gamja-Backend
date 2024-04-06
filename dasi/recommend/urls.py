from django.urls import path
from .views import *

urlpatterns = [
    path('search/', SearchResultCreateView.as_view(), name='search'),
]