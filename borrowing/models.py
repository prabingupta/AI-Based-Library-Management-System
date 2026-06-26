import uuid
from django.db import models
from django.utils import timezone
from accounts.models import User
from books.models import BookCopy
from members.models import Member


class BorrowRecord(models.Model):

    class Status(models.TextChoices):
        BORROWED = 'borrowed', 'Borrowed'
        RETURNED = 'returned', 'Returned'
        OVERDUE = 'overdue', 'Overdue'
        LOST = 'lost', 'Lost'
        RENEWED = 'renewed', 'Renewed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='borrowings')
    book_copy = models.ForeignKey(BookCopy, on_delete=models.PROTECT, related_name='borrowings')
    issued_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='issued_borrowings'
    )
    returned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='received_returns'
    )
    borrow_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.BORROWED)
    renew_count = models.PositiveIntegerField(default=0)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fine_paid = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'borrowing_record'
        verbose_name = 'Borrow Record'
        verbose_name_plural = 'Borrow Records'
        ordering = ['-borrow_date']

    def __str__(self):
        return f"{self.member} - {self.book_copy.book.title} ({self.status})"

    @property
    def is_overdue(self):
        if self.status == self.Status.BORROWED and self.due_date:
            return timezone.now() > self.due_date
        return False

    @property
    def days_overdue(self):
        if self.is_overdue:
            delta = timezone.now() - self.due_date
            return delta.days
        return 0


class Reservation(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        READY = 'ready', 'Ready for Pickup'
        FULFILLED = 'fulfilled', 'Fulfilled'
        CANCELLED = 'cancelled', 'Cancelled'
        EXPIRED = 'expired', 'Expired'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='reservations')
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, related_name='reservations')
    reserved_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'borrowing_reservation'
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
        ordering = ['-reserved_date']

    def __str__(self):
        return f"{self.member} - {self.book_copy.book.title} ({self.status})"


class FineRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    fine_per_day = models.DecimalField(max_digits=6, decimal_places=2, default=5.00)
    max_fine = models.DecimalField(max_digits=8, decimal_places=2, default=500.00)
    grace_period_days = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'borrowing_finerule'
        verbose_name = 'Fine Rule'
        verbose_name_plural = 'Fine Rules'

    def __str__(self):
        return f"{self.name} - Rs.{self.fine_per_day}/day"
