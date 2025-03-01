from rest_framework import serializers
from .models import CustomUser
from django.core.validators import MinLengthValidator

class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

class CustomUserSerializer (serializers.Serializer):

    email = serializers.EmailField()
    passcode =serializers.CharField(max_length=128)  # Hashed version
    bvn =serializers.CharField(max_length=11 )
    nin =serializers.CharField(max_length=11 )
    biometrics =serializers.CharField(max_length=11  )  # Store optional biometric data
    date_of_birth =serializers.DateField( )
    gender =serializers.CharField(max_length=10,  )
    address =serializers.CharField(max_length=11  )
    state_of_origin =serializers.CharField(max_length=50,  )
    nationality =serializers.CharField(max_length=50,  )
    marital_status =serializers.CharField(max_length=20,  )
    is_phone_verified =serializers.BooleanField(default=False)
    email_verification_code =serializers.CharField(max_length=6,  )
    is_email_verified =serializers.BooleanField(default=False)
    authentication_stage =serializers.IntegerField(default=1)

    


class PhoneVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6, required=False)

class EmailSendingSerializer(serializers.Serializer):
    email = serializers.EmailField()
   

class EmailVerificationSerializer(serializers.Serializer):
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
    
