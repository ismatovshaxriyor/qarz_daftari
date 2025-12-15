from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["phone_number", "password"]
        extra_kwargs = {
            "phone_number": {"validators": []}
        }

    def validate_phone_number(self, value):
        if not User.objects.filter(phone_number=value, is_active=False).exists():
            raise serializers.ValidationError(
                "Bu telefon raqam bilan foydalanuvchi topilmadi yoki allaqon faollashtirilgan."
            )
        return value

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        password = validated_data['password']

        try:
            user = User.objects.get(
                phone_number=phone_number,
                is_active=False
            )

            user.set_password(password)
            user.save()

            return user

        except User.DoesNotExist:
            raise serializers.ValidationError({
                "phone_number": "Bu telefon raqami tizimda topilmadi yoki allaqon faollashtirilgan"
            })
        except User.MultipleObjectsReturned:
            raise serializers.ValidationError({
                "phone_number": "Tizimda xatolik yuz berdi"
            })


class UserRegistrationResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()


class RegistrationErrorResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    errorStatus = serializers.CharField(required=False, allow_null=True)
