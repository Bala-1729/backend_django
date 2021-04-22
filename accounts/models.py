from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

class UserProfile(models.Model):
    DeviceId = models.CharField(max_length=256, null=True)
    PhoneNumber = models.CharField(max_length=256, null=True)
    User = models.OneToOneField(User,related_name="UserProfile",on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.User.username

class NPKValues(models.Model):
    n = models.FloatField(null=True)
    p = models.FloatField(null=True)
    k = models.FloatField(null=True)
    deviceId = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.deviceId


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
