from rest_framework import serializers


class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField()
    code = serializers.CharField(max_length=6, min_length=6, required=True, help_text="6 raqamli kod")

    def validate_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("kod faqat raqamlardan iborat bo'lishi kerak")
        return value


class VerifyCodeResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()

    access_token = serializers.CharField(required=False)
    refresh_token = serializers.CharField(required=False)
