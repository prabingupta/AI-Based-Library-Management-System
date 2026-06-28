from celery import shared_task
from django.utils import timezone


@shared_task
def send_due_date_reminders():
    from borrowing.models import BorrowRecord
    from .models import Notification

    tomorrow = timezone.now() + __import__('datetime').timedelta(days=1)
    due_soon = BorrowRecord.objects.filter(
        status='borrowed',
        due_date__date=tomorrow.date()
    ).select_related('member__user', 'book_copy__book')

    count = 0
    for record in due_soon:
        Notification.objects.get_or_create(
            user=record.member.user,
            notification_type='due_date',
            related_object_id=record.pk,
            defaults={
                'title': 'Book Due Tomorrow',
                'message': f'"{record.book_copy.book.title}" is due tomorrow. Please return it on time.',
                'channel': 'in_app',
                'status': 'sent',
            }
        )
        count += 1

    return f'{count} due date reminders sent.'


@shared_task
def mark_overdue_records():
    from borrowing.models import BorrowRecord
    from .models import Notification

    now = timezone.now()
    overdue = BorrowRecord.objects.filter(
        status='borrowed',
        due_date__lt=now
    ).select_related('member__user', 'book_copy__book')

    count = 0
    for record in overdue:
        Notification.objects.get_or_create(
            user=record.member.user,
            notification_type='overdue',
            related_object_id=record.pk,
            defaults={
                'title': 'Book Overdue',
                'message': f'"{record.book_copy.book.title}" is overdue by {record.days_overdue} day(s). Fine may apply.',
                'channel': 'in_app',
                'status': 'sent',
            }
        )
        count += 1

    return f'{count} overdue alerts created.'
