from rest_framework import serializers
from .models import CustomUser
from django.core.validators import MinLengthValidator

class PhoneVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6, required=False)

class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField(max_length=6, required=False)

class PasscodeSetupSerializer(serializers.Serializer):
    passcode = serializers.CharField(max_length=6,
    
    validators=[MinLengthValidator(6)],
    error_messages={
            'min_length': 'Passcode must be exactly 6 digits.',
            'max_length': 'Passcode must be exactly 6 digits.',
        })
    

class BVNVerificationSerializer(serializers.Serializer):
    bvn = serializers.CharField(max_length=11,
    
    
    validators=[MinLengthValidator(11)],
    error_messages={
            'min_length': 'The BVN must be exactly 11 digits.',
            'max_length': 'The BVN must be exactly 11 digits.',
        })
    
