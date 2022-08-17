from ast import Return
from urllib import response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view, APIView
from .models import Post
from .serializers import PostSerializer
from rest_framework import serializers
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import CurrentUserPostsSerializer
from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)

from pyproj import Proj, transform
import pandas as pd
import numpy as np
from django.template import loader

# posts = [
#     {
#         "id": 1,
#         "title": "floor",
#         "content": "This is Floor"
#     },
#     {
#         "id": 2,
#         "title": "Door",
#         "content": "This is Door"
#     },
#     {
#         "id": 3,
#         "title": "Wall",
#         "content": "This is Wall"
#     }
# ]


class PostListCreateView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)
        return super().perform_create(serializer)

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PostRetrieveUpdateDeleteView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# class PostListCreateView(APIView):
#     serializer_class = PostSerializer

#     def get(self, request: Request, *args, **kwargs):
#         posts = Post.objects.all()

#         serializer = PostSerializer(instance=posts, many=True)

#         return Response(data=serializer.data, status=status.HTTP_200_OK)

#     def post(self, reqeust: Request, *args, **kwargs):
#         data = reqeust.data

#         serializers = self.serializer_class(data=data)

#         if serializers.is_valid():
#             serializers.save()

#             response = {
#                 "message": "Post Created",
#                 "data": serializers.data
#             }
#             return Response(data=response, status=status.HTTP_201_CREATED)


# class PostRetrieveUpdateDeleteView(APIView):
#     serializer_class = PostSerializer

#     def get(self, request: Request, post_id: int):
#         post = get_object_or_404(Post, pk=post_id)

#         serializers = self.serializer_class(instance=post)

#         return Response(data=serializers.data, status=status.HTTP_200_OK)

#     def put(self, request: Request, post_id: int):
#         post = get_object_or_404(Post, pk=post_id)

#         data = request.data

#         serializer = self.serializer_class(instance=post, data=data)

#         if serializer.is_valid():
#             serializer.save()

#             response = {
#                 "message": "Post Updated",
#                 "data": serializer.data
#             }
#             return Response(data=response, status=status.HTTP_200_OK)

#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request: Request, post_id: int):
#         post = get_object_or_404(Post, pk=post_id)

#         post.delete()

#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(http_method_names=["GET", "POST"])
def homepage(request):
    # 위경도 좌표 -> 국가지점번호로 변경
    # UTM-K
    # UTM-K(Bassel) 도로명주소 지도 사용
    proj_UTMK = Proj(init='epsg:5178')
    # WGS1984
    # Wgs84 경도/위도, GPS 사용 전지구 좌표
    proj_WGS84 = Proj(init='epsg:4326')

    # UTM-K > WGS84
    x1, y1 = 1387403.7918629837, 1924997.6595098642
    x2, y2 = transform(proj_UTMK, proj_WGS84, x1, y1)
    print(x2, y2)

    # WGS84 -> UTM-K 샘플
    x1, y1 = 37.24334613514286, 131.86684209371853
    y2, x2 = transform(proj_WGS84, proj_UTMK, y1, x1)
    print(x2, y2)

    code = converterToCbc(x2, y2)
    print(code)
    converterToLatLang(code)

    # if request.method == "POST":
    #    data = request.data
    #    response = {"message": "Hello World", "data": data}
    #    return Response(data=response, status=status.HTTP_201_CREATED)

    response = {"message": "Hello World"}
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def converterToCbc(Latitude, hardness):
    wp = Latitude / 100000
    hp = hardness / 100000
    # print("wp : " + str(wp))
    # print("hp : " + str(hp))
    # print(type(w))

    intWP = int(wp)
    intHP = int(hp)

    print(wp[intWP])
    print(hp[intHP])

    first_number = int((Latitude % 100000) / 10)
    second_number = int((hardness % 100000) / 10)
    # print(first_number)
    # print(second_number)

    w_dict = {7: "가", 8: "나", 9: "다", 10: "라", 11: "마", 12: "바", 13: "사"}
    h_dict = {13: "가", 14: "나", 15: "다", 16: "라",
              17: "마", 18: "바", 19: "사", 20: "아"}

    code = str(w_dict[intWP]) + str(h_dict[intHP])

    # print(code)
    return code

# 국가지점번호에서 위경도 좌표


def converterToLatLang(code):
    # 위경도 좌표 -> 국가지점번호로 변경
    # UTM-K
    # UTM-K(Bassel) 도로명주소 지도 사용
    proj_UTMK = Proj(init='epsg:5179')
    # WGS1984
    # Wgs84 경도/위도, GPS 사용 전지구 좌표
    proj_WGS84 = Proj(init='epsg:4326')

    w_dict = {7: "가", 8: "나", 9: "다", 10: "라", 11: "마", 12: "바", 13: "사"}
    h_dict = {13: "가", 14: "나", 15: "다", 16: "라",
              17: "마", 18: "바", 19: "사", 20: "아"}

    first_str = code[0]
    print("frist str " + first_str)
    second_str = code[1]
    print("second_str " + second_str)
    context = code.split()
    first_number = context[1]
    print(first_number)
    second_number = context[2]
    print(second_number)

    w_number = 0
    h_number = 0
    for key, value in w_dict.items():
        if first_str == value:
            print("key : " + str(key))
            w_number = int(key)

    for key, value in h_dict.items():
        if second_str == value:
            print("key : " + str(key))
            h_number = int(key)

    # 길이
    w_length = len(str(w_number)) - 1
    print(w_length)

    # lat*100000+1234+5(marker의 중앙을 맞춰주기 위해서), lng도 동일한 로직
    # 계산 위도
    lat = (pow(10, 6 - w_length) * w_number) + (int(first_number) * 10)
    print(lat)

    # 길이
    h_length = len(str(h_number)) - 1
    print(h_length)

    # 계산 위도
    lng = (pow(10, 6 - h_length) * h_number) + (int(second_number) * 10)
    print(lng)

    print(transform(proj_UTMK, proj_WGS84, lng, lat))


@ api_view(http_method_names=["GET", "POST"])
def list_posts(request: Request):
    posts = Post.objects.all()
    if request.method == "GET":
        serializers = PostSerializer(instance=posts, many=True)
        response = {
            "message": "GET All",
            "data": serializers.data
        }
        return Response(data=response, status=status.HTTP_200_OK)

    elif request.method == "POST":
        data = request.data

        serializers = PostSerializer(data=data)

        if serializers.is_valid():
            serializers.save()

            response = {
                "message": "Post Created",
                "data": serializers.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(data={"error": "post not found"}, status=status.HTTP_404_NOT_FOUND)


@ api_view(http_method_names=["GET"])
def post_detail(request: Request, post_id: int):
    if request.method == "GET":
        posts = Post.objects.filter(id=post_id)
        serializers = PostSerializer(instance=posts, many=True)
        response = {
            "message": "posts",
            "data": serializers.data
        }
        return Response(data=response, status=status.HTTP_200_OK)
    else:
        return Response(data={"error": "post not found"}, status=status.HTTP_404_NOT_FOUND)


@ api_view(http_method_names=["PUT"])
def update_post(request: Request, post_id: int):
    post = get_object_or_404(Post, pk=post_id)

    data = request.data

    serializers = PostSerializer(instance=post, data=data)

    if serializers.is_valid():
        serializers.save()

        response = {
            "message": "Post Updated Successfully",
            "data": serializers.data,
        }

        return Response(data=response, status=status.HTTP_200_OK)

    return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(http_method_names=["DELETE"])
def delete_post(request: Request, post_id: int):
    post = get_object_or_404(Post, pk=post_id)

    post.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@ api_view(http_method_names=['GET'])
@ permission_classes([IsAuthenticated])
def get_posts_for_current_user(request: Request):
    user = request.user

    serializer = CurrentUserPostsSerializer(instance=user)

    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )
