
import random
from django.shortcuts import render
from django.core.cache import cache
# Create your views here.
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import PhoneVerificationSerializer, EmailVerificationSerializer
from django.contrib.auth.hashers import make_password

class PhoneVerificationView(APIView):
    def post(self, request):
        serializer = PhoneVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            user = CustomUser.objects.filter(phone_number=phone_number).first()

            if user:
                if user.is_phone_verified:
                    return Response({'message': 'Phone number is already verified. Proceed to the next authentication step.'}, status=status.HTTP_200_OK)
                
                # If user exists but phone number is not verified, proceed with OTP verification
                return Response({'message': 'User already exists. Please verify your phone number with the OTP sent.'}, status=status.HTTP_200_OK)

            # If no user found, create a new user
            user = CustomUser.objects.create(
                username=phone_number,  # You can customize this as needed
                phone_number=phone_number,
                authentication_stage=1,  # Start at the first stage (phone verification)
            )
            user.save()
            user.save()
            print(f"New user created with phone number: {phone_number}")
            otp = random.randint(100000, 999999)
        
        # Store OTP and phone number in cache for 5 minutes
            cache_key = f"otp_{phone_number}"
            cache.set(cache_key, otp, timeout=300)  # 300 seconds = 5 minutes
        
        
            print(f"OTP for {phone_number} is {otp}")
            return Response({'message': f'OTP sent to phone number.{otp}'}, status=status.HTTP_200_OK)
            # return Response({'message': 'User already exists. Please verify your phone number with the OTP sent.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyPhoneOTPView(APIView):
    def post(self, request):
        serializer = PhoneVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = serializer.validated_data.get('otp')
            print(f"phone number :{phone_number}")
            cache_key = f"otp_{phone_number}"
            print(f"cache key :{cache_key}")
            cached_otp = cache.get(cache_key)
            print(f"otp {cached_otp}")
        
            if cached_otp is None:
                return Response({'error': 'OTP expired or invalid.'}, status=status.HTTP_400_BAD_REQUEST)
        
            if str(cached_otp) == str(otp):
            # OTP is valid
                # return Response({'message': 'Phone number verified successfully.'}, status=status.HTTP_200_OK)
            # Validate OTP logic here
                user = CustomUser.objects.filter(phone_number=phone_number).first()
                print (f"user {user}")
                if user:  # Replace with OTP validation logic
                    user.is_phone_verified = True
                    user.authentication_stage = 2
                    user.save()
            
                    return Response({'message': 'Phone number verified.'}, status=status.HTTP_200_OK)
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

            
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SendEmailVerificationView(APIView):
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.filter(email=email).first()
            if user:
                user.generate_email_verification_code()
                # Send email with the verification code
                send_mail(
                    'Your Email Verification Code',
                    f'Your verification code is {user.email_verification_code}',
                    'no-reply@yourdomain.com',
                    [email],
                )
                return Response({'message': 'Verification code sent to email.'}, status=status.HTTP_200_OK)
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            verification_code = serializer.validated_data['verification_code']
            user = CustomUser.objects.filter(email=email).first()
            if user and user.email_verification_code == verification_code:
                user.is_email_verified = True
                user.authentication_stage = 3  # Progress to the next stage
                user.save()
                return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasscodeSetupView(APIView):
    def post(self, request):
        serializer = PasscodeSetupSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.passcode = make_password(serializer.validated_data['passcode'])
            user.authentication_stage = 4
            user.save()
            return Response({'message': 'Passcode set successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.


class BVNVerificationView(APIView):
    def post(self, request):
        serializer = BVNVerificationSerializer(data=request.data)
        if serializer.is_valid():
            bvn = serializer.validated_data['bvn']
            # Call external API to validate BVN and fetch details
            # response = call_bvn_api(bvn)
            # Mocked response:
            response = {
                'status': 'success',
                'data': {
                    'dob': '1990-01-01',
                    'gender': 'Male',
                    'address': '123 Street Name',
                    'state_of_origin': 'Lagos',
                    'nationality': 'Nigerian',
                    'marital_status': 'Single',
                }
            }
            if response['status'] == 'success':
                user = request.user
                user.bvn = bvn
                user.date_of_birth = response['data']['dob']
                user.gender = response['data']['gender']
                user.address = response['data']['address']
                user.state_of_origin = response['data']['state_of_origin']
                user.nationality = response['data']['nationality']
                user.marital_status = response['data']['marital_status']
                user.authentication_stage = 5
                user.save()
                return Response({'message': 'BVN validated and details saved.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid BVN'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
