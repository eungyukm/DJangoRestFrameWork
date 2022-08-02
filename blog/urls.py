from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from blog.views import PostViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("", PostViewset, basename="posts")

urlpatterns = [
    path('admin', admin.site.urls),
    path('posts/', include(router.urls))
]
