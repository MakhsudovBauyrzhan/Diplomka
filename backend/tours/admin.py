from django.contrib import admin
from .models import Tour, Participation


class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 0
    readonly_fields = ('joined_at',)


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'city', 'start_date', 'end_date', 'max_participants', 'status')
    list_filter = ('status', 'city')
    search_fields = ('title', 'description', 'city', 'author__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ParticipationInline]
    date_hierarchy = 'start_date'


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'status', 'payment_status', 'joined_at')
    list_filter = ('status', 'payment_status')
    search_fields = ('user__email', 'tour__title')
    readonly_fields = ('joined_at',)
