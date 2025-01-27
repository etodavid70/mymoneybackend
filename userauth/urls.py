from django.urls import path
from .views import (
    PhoneVerificationView, VerifyPhoneOTPView, PasscodeSetupView, BVNVerificationView, SendEmailVerificationView, VerifyEmailView
)

urlpatterns = [
    path('phone/', PhoneVerificationView.as_view(), name='phone-verification'),
    path('verify-phone/', VerifyPhoneOTPView.as_view(), name='verify-phone'),
    path('passcode/', PasscodeSetupView.as_view(), name='passcode-setup'),
    path('bvn/', BVNVerificationView.as_view(), name='bvn-verification'),
    path('send-email/', SendEmailVerificationView.as_view(), name='send-email-verification'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email')
]
