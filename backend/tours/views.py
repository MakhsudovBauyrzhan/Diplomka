from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Tour, Participation
from .serializers import (
    TourListSerializer,
    TourDetailSerializer,
    TourCreateUpdateSerializer,
    ParticipationSerializer
)
from .permissions import IsAuthorOrReadOnly


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TourListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return TourCreateUpdateSerializer
        return TourDetailSerializer
    
    def get_queryset(self):
        queryset = Tour.objects.all()
        
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by region
        region = self.request.query_params.get('region', None)
        if region:
            queryset = queryset.filter(region=region)
        
        # Filter by city
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city=city)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date and end_date:
            queryset = queryset.filter(
                start_date__gte=start_date,
                end_date__lte=end_date
            )
        
        # Filter by difficulty level
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        tour = self.get_object()
        
        # Check if tour is full
        if tour.is_full:
            return Response(
                {"detail": "Tour is full"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if tour is in the past
        if tour.is_past:
            return Response(
                {"detail": "Cannot join past tours"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user is already participating
        if Participation.objects.filter(tour=tour, user=request.user).exists():
            return Response(
                {"detail": "Already participating in this tour"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create participation
        participation = Participation.objects.create(
            tour=tour,
            user=request.user,
            status='pending'
        )
        
        return Response(
            ParticipationSerializer(participation).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        tour = self.get_object()
        
        try:
            participation = Participation.objects.get(
                tour=tour,
                user=request.user
            )
            participation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Participation.DoesNotExist:
            return Response(
                {"detail": "Not participating in this tour"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_tours(self, request):
        user = request.user
        tours = Tour.objects.filter(author=user).order_by('-created_at')
        serializer = TourListSerializer(tours, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def participating(self, request):
        user = request.user
        participations = Participation.objects.filter(user=user).values_list('tour_id', flat=True)
        tours = Tour.objects.filter(id__in=participations).order_by('-created_at')
        serializer = TourListSerializer(tours, many=True)
        return Response(serializer.data)


class ParticipationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ParticipationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Tour authors can see all participants, users can only see their own participations
        user = self.request.user
        if 'tour_pk' in self.kwargs:
            tour = get_object_or_404(Tour, pk=self.kwargs['tour_pk'])
            if tour.author == user:
                return Participation.objects.filter(tour=tour)
            else:
                return Participation.objects.filter(tour=tour, user=user)
        return Participation.objects.filter(user=user)
