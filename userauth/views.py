
import random
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
from django.db import IntegrityError
from django.shortcuts import render
from django.core.cache import cache
# Create your views here.
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
 
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import PhoneVerificationSerializer, EmailVerificationSerializer,PasscodeSetupSerializer,BVNVerificationSerializer, EmailSendingSerializer, PhoneSerializer, CustomUserSerializer
from django.contrib.auth.hashers import make_password

class PhoneVerificationView(APIView):
    def post(self, request):
        serializer =PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user = CustomUser.objects.filter(phone_number=phone_number).first()

            #checks if the user exists
            if user:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token) 

                # user_data = CustomUserSerializer(user).data

                return Response({'message': 'phone number already exists. Please verify your email.',
                'access_token': access_token,
                # "details": f"{user_data}"
                }, status=status.HTTP_200_OK,)
            # print(f"New user created with phone number: {phone_number}")
            otp = random.randint(100000, 999999)
        
        # Store OTP and phone number in cache for 5 minutes
            cache_key = f"otp_{phone_number}"
            cache.set(cache_key, otp, timeout=300)  # 300 seconds = 5 minutes
        
        
            print(f"OTP for {phone_number} is {otp}")
            return Response({'message': f'OTP sent to phone number. {otp}',
           
            
            }, status=status.HTTP_200_OK)
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
                user = CustomUser.objects.create(
                # username=phone_number,  # You can customize this as needed
                phone_number=phone_number,
                authentication_stage=2,  # Start at the first stage (phone verification)
                 email=None, 
                 is_phone_verified=True
            )

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token) 
               
                # user.is_phone_verified = True
                # user.authentication_stage = 2
                # user.save()
                # token, _ = Token.objects.get_or_create(user=user)

        
                return Response({'message': 'Phone number verified and saved',
                'access_token': access_token
                
                }, status=status.HTTP_200_OK)
                # return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

            
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SendEmailVerificationView(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializer = EmailSendingSerializer(data=request.data)
            if serializer.is_valid():           
                email = serializer.validated_data['email']
                user= request.user
                user_email = CustomUser.objects.filter(email=user.email).first()
                #this creates an email verification code and saves for the user           
                user.generate_email_verification_code()
                # Send email with the verification code
                    #and bind the code to the email, save this email temporarily
                user.email=email
                user.save()
                    
                return Response({'message': f'Verification code sent to email.  {user.email_verification_code}'}, status=status.HTTP_200_OK)
                # return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
                return Response({"error": "email is used already"}, status= status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            
            verification_code = serializer.validated_data['verification_code']
            user = request.user
            print(user.email)
            # print(verification_code, user.email_verification_code)
            if user and user.email_verification_code == verification_code:
                
                
                user.is_email_verified = True
                user.authentication_stage = 3 
                try:
                # Attempt to save the user
                    user.save()
                    return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
                except IntegrityError as e:
                # Handle the IntegrityError (e.g., unique constraint violation for email)
                    return Response(
                    {'error': f'this email has been used: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST)
                # Progress to the next stage
            return Response({'error': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasscodeSetupView(APIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = BVNVerificationSerializer(data=request.data)
        if serializer.is_valid():
            bvn = serializer.validated_data['bvn']
            # Call external API to validate BVN and fetch details
        
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
