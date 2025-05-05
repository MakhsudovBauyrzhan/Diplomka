from django.db import models
from django.conf import settings
from django.utils import timezone


class Tour(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    # Basic Information
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tours')
    
    # Location Information
    city = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    region = models.CharField(max_length=50, choices=(
        ('north', 'North KZ'),
        ('south', 'South KZ'),
        ('east', 'Eastern KZ'),
        ('west', 'West KZ'),
    ))
    
    # Tour Details
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_participants = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='tours/', blank=True, null=True)
    
    # Additional Information
    difficulty_level = models.CharField(max_length=20, choices=(
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ))
    duration = models.CharField(max_length=50, help_text="e.g., '3 days', '1 week'")
    requirements = models.TextField(blank=True, help_text="What participants need to bring/prepare")
    included = models.TextField(blank=True, help_text="What's included in the price")
    not_included = models.TextField(blank=True, help_text="What's not included in the price")
    
    # Status and Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date")
        if self.max_participants < 1:
            raise ValidationError("Maximum participants must be at least 1")
        if self.price < 0:
            raise ValidationError("Price cannot be negative")
    
    @property
    def is_full(self):
        return self.participants.count() >= self.max_participants
    
    @property
    def available_spots(self):
        return max(0, self.max_participants - self.participants.count())
    
    @property
    def is_past(self):
        return self.end_date < timezone.now()
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['region']),
            models.Index(fields=['start_date']),
        ]


class Participation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('tour', 'user')
    
    def __str__(self):
        return f"{self.user.email} - {self.tour.title}"
