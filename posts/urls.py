from . import views
from django.urls import path

urlpatterns = [
    path("hompage/", views.homepage, name="posts_home"),
    path("", views.PostListCreateView.as_view(), name="list_posts"),
    path("<int:pk>", views.PostRetrieveUpdateDeleteView.as_view(),
         name="list_post"),
    path("<int:pk>", views.PostRetrieveUpdateDeleteView.as_view(),
         name="post_detail"),


    # path("", views.list_posts, name="list_posts"),
    # path("<int:post_id>", views.post_detail, name="post_detail"),
    # path("update/<int:post_id>/", views.update_post, name="update_post"),
    # path("delete/<int:post_id>/", views.delete_post, name="delete_post"),
]
