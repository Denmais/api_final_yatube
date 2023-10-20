from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from posts.models import Post, Comment, Group, Follow
from api.serializers import (PostSerializer, CommentSerializer,
                             GroupSerializer, FollowingSerializer)
from posts.permissions import AuthorOrReadOnly, ReadOnly
from rest_framework import filters
from rest_framework import mixins


class CreateRerieveViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                           mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pass


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


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для групп."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None
    permission_classes = (ReadOnly,)


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


class FollowViewSet(CreateRerieveViewSet):
    serializer_class = FollowingSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', 'user__username')

    def get_queryset(self):
        comment = Follow.objects.filter(user=self.request.user)
        return comment

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
