from django.urls import path
from .views import UserRegistrationView,AccountVerifyCodeView,ResendEmailCodeView,ProtectedView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-account/',AccountVerifyCodeView.as_view(),name="verify-account"),
    path('resend-code/',ResendEmailCodeView.as_view(),name="resend-code"),
    path('protected-view/',ProtectedView.as_view())
]