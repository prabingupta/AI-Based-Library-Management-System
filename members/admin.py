from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['card_number', 'user', 'membership_type', 'status', 'fine_balance', 'created_at']
    list_filter = ['membership_type', 'status']
    search_fields = ['card_number', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Member Info', {
            'fields': ('user', 'card_number', 'membership_type', 'status')
        }),
        ('Membership Period', {
            'fields': ('membership_start', 'membership_end', 'max_books_allowed')
        }),
        ('Financial', {
            'fields': ('fine_balance',)
        }),
        ('Other', {
            'fields': ('address', 'emergency_contact', 'notes', 'is_deleted')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
