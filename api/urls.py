from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )

router = DefaultRouter()
router.register('api/v1/posts', 
                PostViewSet, 
                basename = 'posts')
router.register('api/v1/posts/(?P<post_id>.+)/comments', 
                CommentViewSet, 
                basename='comments')
router.register('api/v1/group', 
                GroupViewSet, 
                basename='groups')
router.register('api/v1/follow', 
                FollowViewSet, 
                basename='follows')


urlpatterns = [
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]

urlpatterns += [
    path('api/v1/api-token-auth/', views.obtain_auth_token)
]