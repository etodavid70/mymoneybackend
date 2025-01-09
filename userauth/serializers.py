from rest_framework import serializers
from .models import CustomUser

class PhoneVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6, required=False)

class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField(max_length=6, required=False)

class PasscodeSetupSerializer(serializers.Serializer):
    passcode = serializers.CharField(max_length=6)

class BVNVerificationSerializer(serializers.Serializer):
    bvn = serializers.CharField(max_length=11)
