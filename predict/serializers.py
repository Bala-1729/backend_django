from rest_framework import serializers
from .models import CropsHistory, NPKValues

class CropsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CropsHistory
        fields = '__all__'

class NPKValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPKValues
        fields = '__all__'
