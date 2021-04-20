from .views import PredictCrop, CropsHistory
from django.urls import path

urlpatterns = [
    path('predict/', PredictCrop.as_view(), name='PredictCrop'),
    path('history/',CropsHistory.as_view(), name="CropsHistory"),
]
