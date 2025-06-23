from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail,EmailMessage

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        string = str(user.pk) + str(timestamp) + str(user.is_active)
        print(string)
        return (
            str(user.pk) + str(timestamp) + str(user.is_active)
        )
    
account_activation_token = AccountActivationTokenGenerator()

def send_verification_email(user,code):

    subject = "Verify your account"
    body = f"Hello {user.first_name} {user.last_name},Thank you for registering.\n\nYour verification code is: {code}"

    email = EmailMessage(
        subject = subject,
        body=body,
        to=[user.email],
    )
    email.send(fail_silently=False)


import random
def generate_4_digit_code():
    return str(random.randint(1000, 9999))
