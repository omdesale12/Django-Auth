from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer,AccountVerifyCodeSerializer,ResendEmailCodeSerializer
from .utils import account_activation_token,send_verification_email,generate_4_digit_code
from .models import EmailVerificationCode,User
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone
from datetime import timedelta

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            code = generate_4_digit_code()
            expires_at = timezone.now() + timedelta(minutes=5)

            EmailVerificationCode.objects.create(
                user = user,
                code = code,
                expires_at = expires_at
            )

            send_verification_email(user,code)
            return Response({
                'message': 'User registered successfully! Check your Email to Verify your Account',
                'email' : user.email
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AccountVerifyCodeView(APIView):
    def post(self,request):
        serializer = AccountVerifyCodeSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error":"Invalid Email"}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                code_record = EmailVerificationCode.objects.get(user = user,code=code)
            except EmailVerificationCode.DoesNotExist:
                return Response({'error': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if code_record.expires_at < timezone.now():
                return Response({'error': 'Verification code expired.'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.is_active = True
            user.save()

            code_record.is_used = True
            code_record.save()

            return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ResendEmailCodeView(APIView):
    def post(self,request):
        serializer = ResendEmailCodeSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "Invalid email."}, status=status.HTTP_404_NOT_FOUND)
            
            if user.is_active:
                return Response({"error": "This account is already verified."}, status=status.HTTP_400_BAD_REQUEST)
            
            EmailVerificationCode.objects.get(user=user).delete()

            code = generate_4_digit_code()
            expires_at = timezone.now() + timedelta(minutes=5)

            EmailVerificationCode.objects.create(
                user=user,
                code=code,
                expires_at=expires_at
            )

            send_verification_email(user,code)

            return Response({"message": "Verification code resent successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        return Response({"message":"Access Granted"})