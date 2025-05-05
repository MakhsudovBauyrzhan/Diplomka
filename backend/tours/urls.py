from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TourViewSet, ParticipationViewSet

router = DefaultRouter()
router.register(r'', TourViewSet, basename='tour')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:tour_pk>/participants/', ParticipationViewSet.as_view({'get': 'list'}), name='tour-participants'),
] 