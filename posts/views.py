from ast import Return
from urllib import response
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


@api_view(http_method_names=["GET", "POST"])
def homepage(request: Request):

    if request.method == "POST":
        data = request.data
        response = {"message": "Hello World", "data": data}
        return Response(data=response, status=status.HTTP_201_CREATED)

    response = {"message": "Hello World"}
    return Response(data=response, status=status.HTTP_200_OK)


@api_view(http_method_names=["GET", "POST"])
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


@api_view(http_method_names=["GET"])
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


@api_view(http_method_names=["PUT"])
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


@api_view(http_method_names=["DELETE"])
def delete_post(request: Request, post_id: int):
    post = get_object_or_404(Post, pk=post_id)

    post.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def get_posts_for_current_user(request: Request):
    user = request.user

    serializer = CurrentUserPostsSerializer(instance=user)

    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )
