from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import Category, Post, Tag, Comment, Like
from .serializers import UserSerializer, CategorySerializer, PostSerializer, TagSerializer, CommentSerializer, LikeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnly, IsCommentOwnerOrReadOnly, IsAdminOrReadOnly, IsLikeOwner
from rest_framework.response import Response

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()          # সবার সব post — কারণ পড়া সবার জন্য open
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'tag']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post']

    def create(self, request, *args, **kwargs):
        post = Post.objects.get(id=request.data.get("post"))
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()   
            return Response({'status': 'unliked'})
        return Response({'status': 'liked'})   
    
    permission_classes = [permissions.IsAuthenticated, IsLikeOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

