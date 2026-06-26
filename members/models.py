import uuid
from django.db import models
from accounts.models import User


class Member(models.Model):

    class MembershipType(models.TextChoices):
        STUDENT = 'student', 'Student'
        TEACHER = 'teacher', 'Teacher'
        GUEST = 'guest', 'Guest'
        STAFF = 'staff', 'Staff'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        SUSPENDED = 'suspended', 'Suspended'
        EXPIRED = 'expired', 'Expired'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    card_number = models.CharField(max_length=50, unique=True)
    membership_type = models.CharField(max_length=20, choices=MembershipType.choices, default=MembershipType.STUDENT)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    membership_start = models.DateField(null=True, blank=True)
    membership_end = models.DateField(null=True, blank=True)
    max_books_allowed = models.PositiveIntegerField(default=3)
    fine_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'members_member'
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name} [{self.card_number}]"

    @property
    def has_overdue_fines(self):
        return self.fine_balance > 0

    @property
    def current_borrow_count(self):
        return self.borrowings.filter(status='borrowed').count()

    @property
    def can_borrow(self):
        return (
            self.status == self.Status.ACTIVE
            and self.current_borrow_count < self.max_books_allowed
            and not self.has_overdue_fines
        )
