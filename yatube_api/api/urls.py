from rest_framework import routers
from django.contrib import admin
from django.urls import include, path
from posts.views import (PostViewSet, CommentViewSet,
                         GroupViewSet, FollowViewSet)


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='comments')
router.register(r'groups', GroupViewSet)
router.register(r'follow', FollowViewSet, basename='following')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
