from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment, Group, Follow
from .serializers import PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
from .permisson import IsAuthorOrReadOnly, PermissionForGroups



class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        group = self.request.query_params.get('group', None)
        if group is not None:
            queryset = queryset.filter(group=group)
        return queryset 


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly,]

    def get_queryset(self, *args, **kwargs):
        post_id = self.kwargs['post_id'] 
        queryset = Comment.objects.filter(post__id=post_id)
        return queryset

    def perform_create(self, serializer, *args, **kwargs):
        post_id = self.kwargs['post_id']
        queryset = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [PermissionForGroups,]

    def perform_create(self, serializer):
        serializer.save()


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ('=user__username', '=following__username')

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(following=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

