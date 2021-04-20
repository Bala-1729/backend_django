from rest_framework import serializers
from .models import CropsHistory

class CropsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CropsHistory
        fields = '__all__'
