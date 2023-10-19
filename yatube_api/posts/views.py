from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from posts.models import Post, Comment, Group, Follow
from api.serializers import (PostSerializer, CommentSerializer,
                             GroupSerializer, FollowingSerializer)
from posts.permissions import AuthorOrReadOnly, ReadOnly
from rest_framework.response import Response
from rest_framework import filters


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class GroupViewSet(viewsets.ModelViewSet):
    """Вьюсет для групп."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None
    permission_classes = (ReadOnly,)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = None
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        comment = Comment.objects.filter(post_id=self.kwargs.get("post_id"))
        return comment

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=Post.objects
                        .get(pk=self.kwargs.get("post_id")))

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowingSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        comment = Follow.objects.filter(user=self.request.user)
        return comment

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
