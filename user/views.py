from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from .models import ZerowaveUser
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import RegisterSerializer

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
def login(request):
    response_data = {}
    
    if request.method == "POST":
        login_email = request.POST.get('email', None)
        login_password = request.POST.get('password', None)

        user = ZerowaveUser.objects.get(email = login_email)
        if not check_password(login_password, user.password) :
            response_data['error'] = "이메일 혹은 비밀번호가 틀렸습니다."
          
        else :
            request.session['user'] = user.id
            
    


def home(request):
    user_id = request.session.get('user')
    if user_id:
        user = ZerowaveUser.objects.get(id = user_id)
        return render(request, 'home.html', {'user': user})
    
    return HttpResponse('로그인을 해주세요.') #session에 user가 없다면, (로그인을 안했다면)


def logout(request):
    del request.session['user']
    return render(request, 'user/successLogout.html') 