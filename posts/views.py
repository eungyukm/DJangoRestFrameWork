from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

posts = [
    {
        "id": 1,
        "title": "floor",
        "content": "This is Floor"
    },
    {
        "id": 2,
        "title": "Door",
        "content": "This is Door"
    },
    {
        "id": 3,
        "title": "Wall",
        "content": "This is Wall"
    }
]


@api_view(http_method_names=["GET", "POST"])
def homepage(request: Request):

    if request.method == "POST":
        data = request.data
        response = {"message": "Hello World", "data": data}
        return Response(data=response, status=status.HTTP_201_CREATED)

    response = {"message": "Hello World"}
    return Response(data=response, status=status.HTTP_200_OK)


@api_view(http_method_names=["GET"])
def list_posts(request: Request):
    return Response(data=posts, status=status.HTTP_200_OK)


@api_view(http_method_names=["GET"])
def post_detail(request: Request, post_id: int):
    post = posts[post_id]

    if post:
        return Response(data=post, status=status.HTTP_200_OK)

    return Response(data={"error": "post not found"}, status=status.HTTP_404_NOT_FOUND)
