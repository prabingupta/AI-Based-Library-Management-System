import uuid
from django.db import models
from django.utils.text import slugify
from accounts.models import User


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='%(class)s_created'
    )

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='FontAwesome icon class')
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'books_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Author(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'books_author'
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        ordering = ['last_name', 'first_name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name} {self.last_name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Publisher(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='publishers/', blank=True, null=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'books_publisher'
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Language(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, help_text='ISO 639-1 code e.g. en, ne, fr')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'books_language'
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Shelf(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    floor = models.CharField(max_length=50, blank=True)
    section = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(default=100)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'books_shelf'
        verbose_name = 'Shelf'
        verbose_name_plural = 'Shelves'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Book(TimeStampedModel):

    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        UNAVAILABLE = 'unavailable', 'Unavailable'
        RESERVED = 'reserved', 'Reserved'
        LOST = 'lost', 'Lost'
        DAMAGED = 'damaged', 'Damaged'
        PROCESSING = 'processing', 'Processing'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=520, unique=True, blank=True)
    isbn = models.CharField(max_length=20, unique=True, blank=True, null=True)
    isbn13 = models.CharField(max_length=20, unique=True, blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='books', blank=True)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='books'
    )
    categories = models.ManyToManyField(Category, related_name='books', blank=True)
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='books'
    )
    cover_image = models.ImageField(upload_to='books/covers/', blank=True, null=True)
    description = models.TextField(blank=True)
    edition = models.CharField(max_length=100, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    shelf = models.ForeignKey(
        Shelf, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='books'
    )
    call_number = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text='Comma separated tags')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    # AI-ready fields
    embedding_vector = models.TextField(blank=True, null=True, help_text='Future: AI embedding vector')
    ai_summary = models.TextField(blank=True, null=True, help_text='Future: AI generated summary')
    ai_tags = models.TextField(blank=True, null=True, help_text='Future: AI generated tags')

    class Meta:
        db_table = 'books_book'
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BookCopy(TimeStampedModel):

    class Condition(models.TextChoices):
        NEW = 'new', 'New'
        GOOD = 'good', 'Good'
        FAIR = 'fair', 'Fair'
        POOR = 'poor', 'Poor'
        DAMAGED = 'damaged', 'Damaged'

    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        BORROWED = 'borrowed', 'Borrowed'
        RESERVED = 'reserved', 'Reserved'
        LOST = 'lost', 'Lost'
        DAMAGED = 'damaged', 'Damaged'
        MAINTENANCE = 'maintenance', 'Maintenance'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copies')
    barcode = models.CharField(max_length=100, unique=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    shelf = models.ForeignKey(
        Shelf, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='copies'
    )
    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.GOOD)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    acquisition_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'books_bookcopy'
        verbose_name = 'Book Copy'
        verbose_name_plural = 'Book Copies'
        ordering = ['barcode']

    def __str__(self):
        return f"{self.book.title} [{self.barcode}]"
