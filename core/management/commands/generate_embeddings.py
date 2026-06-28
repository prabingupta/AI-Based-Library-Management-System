import json
from django.core.management.base import BaseCommand
from django.db.models import Q


class Command(BaseCommand):
    help = "Generate AI embeddings for all books using sentence-transformers"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Regenerate embeddings even if they already exist",
        )

    def handle(self, *args, **options):
        from books.models import Book
        from books.services.recommendation import get_book_text

        try:
            from sentence_transformers import SentenceTransformer

            self.stdout.write("Loading sentence-transformers model...")
            model = SentenceTransformer("all-MiniLM-L6-v2")
            self.stdout.write(self.style.SUCCESS("Model loaded."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to load model: {e}"))
            return

        books = Book.objects.filter(is_deleted=False, is_active=True).prefetch_related("authors", "categories")

        if not options["force"]:
            books = books.filter(Q(embedding_vector__isnull=True) | Q(embedding_vector=""))

        total = books.count()
        if total == 0:
            self.stdout.write(self.style.WARNING("No books need embeddings. Use --force to regenerate."))
            return

        self.stdout.write(f"Generating embeddings for {total} books...")

        success = 0
        failed = 0

        for i, book in enumerate(books, 1):
            try:
                text = get_book_text(book)
                embedding = model.encode(text, convert_to_numpy=True).tolist()
                book.embedding_vector = json.dumps(embedding)
                book.save(update_fields=["embedding_vector"])
                success += 1
                self.stdout.write(f"  [{i}/{total}] ✓ {book.title[:50]}")
            except Exception as e:
                failed += 1
                self.stdout.write(self.style.WARNING(f"  [{i}/{total}] ✗ {book.title[:50]} — {e}"))

        self.stdout.write(self.style.SUCCESS(f"\nDone! {success} embeddings generated. {failed} failed."))
