from rest_framework_nested import routers
from core.user.viewsets import UserViewSet
from core.auth.viewsets import(
    RegisterViewSet, 
    LoginViewSet,
    RefreshViewSet
    )
from core.post.viewsets import PostViewSet
from core.comment.viewsets import CommentViewSet
from core.mediaItems.viewsets import ProcessedMediaItemCallbackViewSet

router = routers.SimpleRouter()

router.register(r'user', UserViewSet, basename='user')
router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewSet, basename='auth-login')
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')
router.register(r'post', PostViewSet, basename='post')
router.register(r'processed_media_callback', ProcessedMediaItemCallbackViewSet, basename='processed_media_callback')

# comment router 
# The resulting URL patterns will include routes for the main router and the nested router, with the following structure:
# Main router:
# /post/ - Handles CRUD operations for posts.
# Nested router:
# /post/{post_pk}/comment/ - Handles CRUD operations for comments associated with a specific post.
posts_router = routers.NestedSimpleRouter(router, r'post', lookup='post')
posts_router.register(r'comment', CommentViewSet, basename='post-comment')
# posts_router.register(r'media-items', MediaItemUploadView, basename='post-media-items')
urlpatterns = [
   *router.urls,
   *posts_router.urls
]