from .views import PredictCrop, CropsHistory, NPKView
from django.urls import path

urlpatterns = [
    path('predict/', PredictCrop.as_view(), name='PredictCrop'),
    path('history/',CropsHistory.as_view(), name="CropsHistory"),
    path('npk-value/', NPKView.as_view(), name="npkvalues")
]
