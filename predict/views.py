from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CropsHistorySerializer
from .models import CropsHistory as cs
import sys
import pickle
import numpy as np
from twilio.rest import Client

crops=['wheat','mungbean','Tea','millet','maize','lentil','jute','cofee','cotton','ground nut','peas','rubber','sugarcane','tobacco','kidney beans','moth beans','coconut','blackgram','adzuki beans','pigeon peas','chick peas','banana','grapes','apple','mango','muskmelon','orange','papaya','watermelon','pomegranate']

model=pickle.load(open('model.pkl','rb'));
model1=pickle.load(open('model1.pkl','rb'))

class PredictCrop(APIView):
    def post(self, request):
        obj=self.request.data
        serializer = CropsHistorySerializer(data=self.request.data)
        data = [obj[i] for i in obj]
        output=""
        if "" in data:
            output=predictor(data[:4])
        else:
            output=predictor(data)
        if serializer.is_valid():
            serializer.save(user=self.request.user,crop=output)
        return Response({'crop':output})


class CropsHistory(APIView):
    def get(self,request):
        cropData = cs.objects.filter(user=self.request.user)
        length=len(cropData)
        serializer=CropsHistorySerializer(cropData,many=True)
        return Response({"CropsHistory":serializer.data})

def predictor(data):
    x_test = data
    sample = np.array(x_test).reshape(1,-1)
    print("sample: ",sample)
    prediction=model.predict(sample) if len(data)==4 else model1.predict(sample)
    return prediction[0]
