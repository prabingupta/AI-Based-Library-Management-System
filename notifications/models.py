import uuid
from django.db import models
from accounts.models import User


class Notification(models.Model):

    class NotificationType(models.TextChoices):
        DUE_DATE = 'due_date', 'Due Date Reminder'
        OVERDUE = 'overdue', 'Overdue Alert'
        RESERVATION_READY = 'reservation_ready', 'Reservation Ready'
        FINE_ISSUED = 'fine_issued', 'Fine Issued'
        FINE_PAID = 'fine_paid', 'Fine Paid'
        BOOK_AVAILABLE = 'book_available', 'Book Available'
        MEMBERSHIP_EXPIRY = 'membership_expiry', 'Membership Expiring'
        GENERAL = 'general', 'General'

    class Channel(models.TextChoices):
        EMAIL = 'email', 'Email'
        SMS = 'sms', 'SMS'
        PUSH = 'push', 'Push Notification'
        IN_APP = 'in_app', 'In-App'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SENT = 'sent', 'Sent'
        FAILED = 'failed', 'Failed'
        READ = 'read', 'Read'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices)
    channel = models.CharField(max_length=20, choices=Channel.choices, default=Channel.IN_APP)
    title = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    related_object_id = models.UUIDField(null=True, blank=True)
    related_object_type = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notifications_notification'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.title} ({self.status})"
