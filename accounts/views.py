from django.contrib.auth import login

from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer, UserProfileSerializer, NPKValuesSerializer
from django.views.decorators.debug import sensitive_post_parameters
from .models import UserProfile as us
from .models import NPKValues as n
from rest_framework.views import APIView
import pickle
import numpy as np
from twilio.rest import Client

crops=['wheat','mungbean','Tea','millet','maize','lentil','jute','cofee','cotton','ground nut','peas','rubber','sugarcane','tobacco','kidney beans','moth beans','coconut','blackgram','adzuki beans','pigeon peas','chick peas','banana','grapes','apple','mango','muskmelon','orange','papaya','watermelon','pomegranate']

model=pickle.load(open('model.pkl','rb'));

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

#Register DeviceId
class RegisterDeviceAPI(APIView):
    def post(self, request):
        serializer = UserProfileSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save(User=self.request.user)
        return Response({"message":"success"}, status=status.HTTP_201_CREATED)

# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

#Load data
class LoadDataView(APIView):
    array={"temperature":"please reload", "humidity":"please reload", "ph":"please reload","moisture":"please reload"}
    def get(self,request):
        return Response({"values":self.array})

    def post(self,request):
        self.array["temperature"]=self.request.data["temperature"]
        self.array["humidity"]=self.request.data["humidity"]
        self.array["ph"]=self.request.data["ph"]
        self.array["moisture"]=self.request.data["moisture"]
        output=str(predictor([self.request.data["temperature"], self.request.data["humidity"], self.request.data["ph"], self.request.data["moisture"]]))
        return Response({"crop":output})

#SMS View
class SmsView(APIView):
    def post(self,request):
        output=str(predictor([self.request.data["temperature"], self.request.data["humidity"], self.request.data["ph"], self.request.data["moisture"]]))
        account_sid = 'ACc1770c958b407cedb310af918786da04'
        auth_token = '89f98a027cfafd65fbe4178f9432c429'
        client = Client(account_sid, auth_token)
        user = UserProfile.objects.get(DeviceId=self.request.data["deviceId"])
        message = client.messages.create(body="Predicted Crop:"+output,from_='+13012468250',to="+91"+user.PhoneNumber)
        return Response({"crop":output})

class NPKValues(APIView):
    def get(self, request):
        npkValues = n.objects.filter(deviceId=self.request.headers.get("deviceId"))
        user = us.objects.get(DeviceId=self.request.headers.get("deviceId"))
        if not npkValues:
            return Response({"message":"create Entries First"})
        serializer=NPKValuesSerializer(npkValues,many=True)
        return Response(serializer.data[-1])

    def post(self,request):
        obj=self.request.data
        serializer = NPKValuesSerializer(data=self.request.data)
        data = [obj[i] for i in obj]
        user = us.objects.get(User=self.request.user)
        if serializer.is_valid():
            serializer.save(deviceId=user.DeviceId)

        return Response({"success"})


def predictor(data):
    x_test = data
    sample = np.array(x_test).reshape(1,-1)
    prediction=model.predict(sample)
    return prediction[0]
# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

from rest_framework import generics, permissions

# Change Password
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
