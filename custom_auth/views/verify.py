from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse

from custom_auth.serializers import VerifyCodeSerializer, VerifyCodeResponseSerializer, ErrorResponseSerializer


User = get_user_model()

class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=VerifyCodeSerializer,
        responses={
            200: OpenApiResponse(
                response=VerifyCodeResponseSerializer,
                description="Akkount aktivlashtirildi"
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description='Parol noto\'g\'ri yoki validatsiya xatosi'
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer,
                description='User topilmadi'
            )
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)

        if not serializer.is_valid():
            error = serializer.errors
            first_field = next(iter(error))
            error_msg = error[first_field][0]

            return Response(
                {
                    "success": False,
                    "message": error_msg,
                    "errorStatus": 'data_credential'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        try:
            user = User.objects.get(phone_number=phone_number)
            cache_key = f"activation_code_{user.id}"

            cached_data = cache.get(cache_key)

            if not cached_data:
                return Response(
                    {
                        "success": False,
                        "message": 'Kod eskirgan. Ynagi kod so\'rang',
                        "errorStatus": 'time_out'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if cached_data.get('code') != code:
                return Response(
                    { 'success': False, 'error': 'Noto\'g\'ri kod', 'errorStatus': 'data_credential'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cache.delete(cache_key)

            user.is_active = True
            user.save()

            tokens = RefreshToken.for_user(user)
            response_data = {
                'success': True,
                'message': 'Akkount muvaffaqiyatli aktivlashtirildi',
                'response': {
                    'access': str(tokens.access_token),
                    'refresh': str(tokens),
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "User topilmadi",
                    "errorStatus": "data_credential"
                }
            )

