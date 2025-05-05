from rest_framework import serializers
from .models import Tour, Participation
from django.contrib.auth import get_user_model

User = get_user_model()


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'avatar']


class ParticipationSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = Participation
        fields = ['id', 'user', 'status', 'payment_status', 'joined_at']
        read_only_fields = ['id', 'user', 'joined_at']


class TourListSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer(read_only=True)
    available_spots = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Tour
        fields = [
            'id', 'title', 'city', 'region', 'description', 'image', 'author',
            'start_date', 'end_date', 'max_participants', 'price',
            'available_spots', 'is_full', 'status', 'created_at',
            'difficulty_level', 'duration'
        ]
        read_only_fields = ['id', 'author', 'created_at']


class TourDetailSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer(read_only=True)
    participants = ParticipationSerializer(many=True, read_only=True)
    available_spots = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    is_past = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Tour
        fields = [
            'id', 'title', 'description', 'author',
            'city', 'region', 'location', 'image',
            'start_date', 'end_date', 'max_participants', 'price',
            'status', 'created_at', 'updated_at',
            'available_spots', 'is_full', 'is_past',
            'participants', 'difficulty_level', 'duration',
            'requirements', 'included', 'not_included'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class TourCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = [
            'title', 'description', 'city', 'region', 'location',
            'start_date', 'end_date', 'max_participants', 'price', 
            'image', 'status', 'difficulty_level', 'duration',
            'requirements', 'included', 'not_included'
        ]
    
    def validate(self, attrs):
        # Ensure end_date is after start_date
        if 'start_date' in attrs and 'end_date' in attrs:
            if attrs['end_date'] <= attrs['start_date']:
                raise serializers.ValidationError({"end_date": "End date must be after start date"})
        
        # Ensure max_participants is positive
        if 'max_participants' in attrs and attrs['max_participants'] <= 0:
            raise serializers.ValidationError({"max_participants": "Maximum participants must be greater than 0"})
        
        # Ensure price is non-negative
        if 'price' in attrs and attrs['price'] < 0:
            raise serializers.ValidationError({"price": "Price cannot be negative"})
        
        return attrs 