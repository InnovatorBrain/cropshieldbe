from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from rest_framework import serializers
from rest_framework import serializers
from .models import CustomUser as User
from django.utils.encoding import force_str
from rest_framework.exceptions import ValidationError
from .utils import Util 

# Email import
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError 
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "confirm_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data["password"] != data.pop("confirm_password"):
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            username=validated_data["email"],  # Use email as username
            password=validated_data["password"],
        )
        return user

class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def send_verification_email(self, user):
        current_site = get_current_site(self.context['request'])
        mail_subject = 'Activate your account'
        message = render_to_string('registration/verification_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = self.validated_data['email']
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self, **kwargs):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        self.send_verification_email(user)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'is_active']
        read_only_fields = ['is_active', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'read_only': True},
        }

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)
    
"""Password Change Serializer
"""
class CustomPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, style={'input_type': 'password'}, write_only=True) 
    confirm_password = serializers.CharField(max_length=128, style={'input_type': 'password'}, write_only=True) 

    class Meta:
        fields = ['password', 'confirm_password']
    
    def create(self, validated_data):
        user = self.context['user']
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        user = self.context.get('user')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        user.set_password(password)
        user.save()
        return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    
    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            link = f"http://127.0.0.1:8000/auth/reset-password-Email/{uid}/{token}"
            print(f"Password Reset Link: {link}")
            
            # Formatting the email body
            recipient_name = user.first_name
            recipient_username = user.username
            sender_name = "CropShield Support"
            sender_position = ""
            sender_contact = "support@cropshield.com"
            body = self.format_body(recipient_name, recipient_username, link, sender_name, sender_position, sender_contact)

            mail_subject = 'Password Reset Request'
            data = {
                'email_subject': mail_subject,
                'email_body': body,
                'to_email': user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError("User with this email does not exist.")
        
    def create(self, validated_data):
        return {}
        
    def format_body(self, recipient_name, recipient_username, link, sender_name, sender_position, sender_contact):
        body = f"""
🌾 AI and Blockchain-Based Crop Insurance 🌱 

Dear {recipient_name},

We hope this message finds you well. At CropShield we are committed to protecting your personal information.                    

You have recently initiated a password reset request for your account {recipient_username} on our innovative platform, the "AI and Blockchain-Based Crop Insurance System." To proceed, please follow the link provided below:

{link}
If you have any questions or require further assistance, feel free to contact us at support@cropshield.com. Your satisfaction is our top priority.

Warm regards,
{sender_name}
{sender_position}
"""
        return body

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  confirm_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'confirm_password']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      confirm_password = attrs.get('confirm_password')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != confirm_password:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Password Reset Successfully')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')
    
  def create(self, validated_data):
        return {}