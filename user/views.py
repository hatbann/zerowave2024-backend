from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from .models import ZerowaveUser
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from .serializer import RegisterSerializer, UserProfileSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import  IsAuthenticated
from tokenize import TokenError
from jwt import InvalidTokenError
from django.core.serializers.json import DjangoJSONEncoder
import json

# Create your views here.
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            user = serializer.save()
            # jwt token 접근해주기
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            #쿠키에 넣어주기...아직 어떤식으로 해야될지 모르겠는데 이렇게 설정만 우선 해주었다. 
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthView(APIView):

    def post(self, request):
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    
    
    def patch(self, request, *args, **kwargs):
        serializer_data = request.data
 
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request) -> Response:
        print(request.data)
        refresh_token = request.data.get("refresh")
        data = {"refresh": refresh_token}
        serializer = self.get_serializer(data= data)

        try:
            serializer.is_valid(raise_exception= True)
        except TokenError as e:
            raise InvalidTokenError(e.args[0])

        token = serializer.validated_data
        response = Response({"detail": "refresh success", "access" : token['access'], "refresh" : token['refresh']}, status= status.HTTP_200_OK)

        return response

class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        print(request.user)
        serializer = UserProfileSerializer(request.user)
        return Response({'message': '프로필 가져오기 성공', 'data': serializer.data}, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    def get(self, request, format=None):
        #userpk = request.GET.get('id__in[]')
        if(request.query_params.get('id__in[]')) : 
            userpk = request.query_params.get('id__in[]').split(',')
            list_int = list(map(int, userpk)) # 정수로 변환
            users = ZerowaveUser.objects.values('id', 'nickname').filter(id__in=list_int)
            serialized_q = json.dumps(list(users), cls=DjangoJSONEncoder)
            return Response({'message': '프로필 가져오기 성공', 'data': serialized_q}, status=status.HTTP_200_OK)
        else:
            userpk = request.query_params.get('id')
            user = ZerowaveUser.objects.values('id' , 'nickname').filter(id=userpk)
            serialized_q = json.dumps(list(user), cls=DjangoJSONEncoder)
            return Response({'message': '프로필 가져오기 성공', 'data': serialized_q}, status=status.HTTP_200_OK)

    


def home(request):
    user_id = request.session.get('user')
    if user_id:
        user = ZerowaveUser.objects.get(id = user_id)
        return render(request, 'home.html', {'user': user})
    
    return HttpResponse('로그인을 해주세요.') #session에 user가 없다면, (로그인을 안했다면)


def logout(request):
    del request.session['user']
    return render(request, 'user/successLogout.html') 