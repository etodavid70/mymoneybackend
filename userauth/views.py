from django.shortcuts import render

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
            # Generate OTP and send via SMS (e.g., Twilio)
            # otp = generate_otp()
            # send_sms(phone_number, otp)
            return Response({'message': 'OTP sent to phone number.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyPhoneOTPView(APIView):
    def post(self, request):
        serializer = PhoneVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = serializer.validated_data.get('otp')
            # Validate OTP logic here
            user = CustomUser.objects.filter(phone_number=phone_number).first()
            if user and otp_is_valid(otp):  # Replace with OTP validation logic
                user.is_phone_verified = True
                user.authentication_stage = 2
                user.save()
                return Response({'message': 'Phone number verified.'}, status=status.HTTP_200_OK)
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
