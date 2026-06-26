from django.contrib import admin
from .models import BorrowRecord, Reservation, FineRule


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['member', 'book_copy', 'borrow_date', 'due_date', 'status', 'fine_amount', 'fine_paid']
    list_filter = ['status', 'fine_paid']
    search_fields = ['member__card_number', 'member__user__email', 'book_copy__barcode']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Borrow Info', {
            'fields': ('member', 'book_copy', 'issued_by', 'returned_to')
        }),
        ('Dates', {
            'fields': ('borrow_date', 'due_date', 'return_date')
        }),
        ('Status', {
            'fields': ('status', 'renew_count')
        }),
        ('Fine', {
            'fields': ('fine_amount', 'fine_paid')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['member', 'book_copy', 'reserved_date', 'expiry_date', 'status']
    list_filter = ['status']
    search_fields = ['member__card_number', 'book_copy__barcode']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(FineRule)
class FineRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'fine_per_day', 'max_fine', 'grace_period_days', 'is_active']
    list_filter = ['is_active']
