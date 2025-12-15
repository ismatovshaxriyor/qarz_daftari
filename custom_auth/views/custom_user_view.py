from rest_framework import status
from rest_framework.response import Response
from djoser.views import UserViewSet


class CustomUserViewSet(UserViewSet):

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return Response(
            {"detail": "List endpoint disabled."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "Registration disabled."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def reset_password(self, request, *args, **kwargs):
        return super().reset_password(request, *args, **kwargs)

    def activation(self, request, *args, **kwargs):
        return Response({"detail": "Disabled."}, status=status.HTTP_404_NOT_FOUND)

