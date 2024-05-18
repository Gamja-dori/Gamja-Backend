from rest_framework import serializers
from .models import *

class SearchSerializer(serializers.ModelSerializer):   
    class Meta:
        model = SearchHistory
        fields = "__all__"