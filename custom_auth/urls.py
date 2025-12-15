from django.urls import path, include
from rest_framework.routers import DefaultRouter
from custom_auth.views import *

router = DefaultRouter()
router.register(r'user', CustomUserViewSet, basename='users')

urlpatterns = [
    path('user/register/', UserRegisterView.as_view(), name='user-register'),
    path('user/verify/', VerifyCodeView.as_view(), name='user-verify'),
    path('', include(router.urls)),
]
