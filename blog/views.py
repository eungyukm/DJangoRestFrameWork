from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.request import Request
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework.response import Response


class PostViewset(viewsets.ViewSet):
    def list(self, request: Request):
        queryset = Post.objects.all()
        serializer = PostSerializer(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request: Request, pk=None):
        post = get_object_or_404(Post, pk=pk)

        serializer = PostSerializer(instance=post)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
