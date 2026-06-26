import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        SUPER_ADMIN = 'super_admin', 'Super Admin'
        LIBRARY_ADMIN = 'library_admin', 'Library Admin'
        LIBRARIAN = 'librarian', 'Librarian'
        ASSISTANT_LIBRARIAN = 'assistant_librarian', 'Assistant Librarian'
        TEACHER = 'teacher', 'Teacher'
        STUDENT = 'student', 'Student'
        GUEST = 'guest', 'Guest'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.STUDENT)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'accounts_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    @property
    def full_name(self):
        return self.get_full_name()

    @property
    def is_admin(self):
        return self.role in [self.Role.SUPER_ADMIN, self.Role.LIBRARY_ADMIN]
