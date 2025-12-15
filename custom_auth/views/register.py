import random
import string
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.contrib.auth import get_user_model
from django.core.cache import cache

# import the serializers from the specific module file
from custom_auth.serializers.register import (
    UserRegistrationSerializer,
    RegistrationErrorResponseSerializer,
    UserRegistrationResponseSerializer,
)
from custom_auth.signals import send_code

User = get_user_model()

class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        request=UserRegistrationSerializer,
        responses={
            200: OpenApiResponse(
                response=UserRegistrationResponseSerializer,
                description="User muvaffaqiyatli yaratildi, bot orqali kod yuborildi."
            ),
            400: OpenApiResponse(
                response=RegistrationErrorResponseSerializer,
                description='User yaratishda xatolik yuz berdi.'
            )
        },
        tags=['Authentication']
    )
    def post(self, request):
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")

        if not phone_number or not password:
            return Response(
                {
                    "success": False,
                    "message": "Telefon raqami va parol talab qilinadi",
                    "errorStatus": "missing_fields"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Faol user mavjudligini tekshiramiz
        if User.objects.filter(phone_number=phone_number, is_active=True).exists():
            return Response(
                {
                    "success": False,
                    "message": 'Bu telefon raqami allaqachon ro\'yxatdan o\'tgan',
                    "errorStatus": 'exists'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserRegistrationSerializer(
            data={"phone_number": phone_number, "password": password}
        )

        if not serializer.is_valid():
            errors = serializer.errors
            first_field = next(iter(errors))
            error_msg = errors[first_field][0]

            return Response(
                {
                    "success": False,
                    "message": error_msg,
                    "errorStatus": "data_credential"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()  # ✅ Endi user parol bilan yangilanadi

        # Verification code yuborish
        code = ''.join(random.choices(string.digits, k=6))
        telegram_id = user.telegram_id

        if not telegram_id:
            return Response(
                {
                    "success": False,
                    "message": "Telegram ID topilmadi. Avval /start buyrug'ini yuboring",
                    "errorStatus": "no_telegram_id"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        cache_key = f"activation_code_{user.id}"
        cache_data = {
            "phone": user.phone_number,
            "user_id": user.id,
            "code": code
        }

        cache.set(cache_key, cache_data, 300)

        try:
            send_code(telegram_id, code)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": f"Telegram orqali kod yuborishda xatolik: {str(e)}",
                    "errorStatus": "telegram_error",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response_data = {
            'success': True,
            'message': "Tasdiqlash kodi yuborildi"
        }
        return Response(response_data, status=status.HTTP_200_OK)



