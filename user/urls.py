from django.urls import path, include
from .views import AuthView, RegisterAPIView ,UserRetrieveUpdateAPIView, RegisterAPIView, CustomTokenRefreshView,MyProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from . import views

urlpatterns = [
    path("register/", RegisterAPIView.as_view()), #회원가입하기
    path("login/", AuthView.as_view()),
       path("update/", UserRetrieveUpdateAPIView.as_view()),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", CustomTokenRefreshView.as_view()),
    path("get_user_self/", MyProfileView.as_view()),
    path("get_nickname/", views.UserProfileView.as_view())
]