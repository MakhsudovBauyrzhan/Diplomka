from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import EmailVerification

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'date_of_birth', 
                 'description', 'avatar', 'is_email_verified', 'terms_agreed']
        read_only_fields = ['email', 'is_email_verified']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    terms_agreed = serializers.BooleanField(required=True)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'date_of_birth', 
                 'password', 'password_confirm', 'terms_agreed']
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": _("Password fields didn't match.")})
        
        if not attrs.get('terms_agreed'):
            raise serializers.ValidationError({"terms_agreed": _("You must agree to the terms.")})
            
        if attrs.get('phone') and not attrs['phone'].isdigit():
            raise serializers.ValidationError({"phone": _("Phone number should contain only digits.")})
            
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": _("Password fields didn't match.")})
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Old password is not correct"))
        return value


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'date_of_birth', 
                 'description', 'avatar'] 