from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from .models import BoardModel
from .serializer import PostSerializer

# APIView를 사용하기 위해 import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


class PostList(APIView):
    # lists
    def get(self, request):
        posts = BoardModel.objects.all()
        # 여러 개의 객체를 serialization하기 위해 many=True로 설정
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    # 새 글 작성
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        print(request.user)
        data = {
            'title': request.data.get('title'),
            'content': request.data.get('content'),
            'location': request.data.get('location'),
            'author': request.data.get("author"),
        }
        serializer = PostSerializer(data=data)
        if serializer.is_valid(): #유효성 검사
            serializer.save() # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# detail을 보여주는 역할
class PostDetail(APIView):
    # Post 객체 가져오기
    def get_object(self, pk):
        try:
            return BoardModel.objects.get(pk=pk)
        except BoardModel.DoesNotExist:
            raise Http404
    
    #  detail 보기
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    #  수정하기
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #  삭제하기
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)      
