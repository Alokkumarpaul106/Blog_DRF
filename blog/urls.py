# urls.py
from django.urls import path, include
from blog.views import UserViewSet, CategoryViewSet,PostViewSet,TagViewSet,CommentViewSet,LikeViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
# Initialize the router
router = DefaultRouter()

# Register your ViewSets
router.register(r'users', UserViewSet, basename='user')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'post', PostViewSet, basename='posts')
router.register(r'like', LikeViewSet, basename='likes')
router.register(r'tag', TagViewSet, basename='tags')
router.register(r'comment', CommentViewSet, basename='comments')


# Include the router URLs into your urlpatterns
urlpatterns = [
    path('api/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token)
]
