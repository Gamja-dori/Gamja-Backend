from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.serializers import serialize, deserialize

class SearchSerializer(serializers.ModelSerializer):   
    class Meta:
        model = SearchResult
        fields = "__all__"
        

