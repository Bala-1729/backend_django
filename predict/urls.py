from .views import PredictCrop, CropsHistory, NPKValues
from django.urls import path

urlpatterns = [
    path('predict/', PredictCrop.as_view(), name='PredictCrop'),
    path('history/',CropsHistory.as_view(), name="CropsHistory"),
    path('npk-values/',NPKValues.as_view(), name="NPKValues")
]
