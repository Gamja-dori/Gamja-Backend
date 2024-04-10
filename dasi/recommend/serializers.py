from rest_framework import serializers
from .models import *

class SearchSerializer(serializers.ModelSerializer):   
    class Meta:
        model = SearchResult
        fields = "__all__"


class FilterSerializer(serializers.ModelSerializer):   
    class Meta:
        model = FilterResult
        fields = "__all__"
        

