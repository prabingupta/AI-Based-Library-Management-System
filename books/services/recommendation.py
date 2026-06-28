import json
import numpy as np


def get_book_text(book):
    parts = [book.title]
    for author in book.authors.all():
        parts.append(author.full_name)
    for cat in book.categories.all():
        parts.append(cat.name)
    if book.description:
        parts.append(book.description[:300])
    if book.tags:
        parts.append(book.tags)
    return " ".join(parts)


def generate_embedding(text):
    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
        embedding = model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    except Exception:
        return None


def cosine_similarity(vec_a, vec_b):
    a = np.array(vec_a)
    b = np.array(vec_b)
    dot = np.dot(a, b)
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    if norm == 0:
        return 0.0
    return float(dot / norm)


def get_recommendations(book, top_n=4):
    from books.models import Book

    if not book.embedding_vector:
        return _fallback_recommendations(book, top_n)

    try:
        target_vec = json.loads(book.embedding_vector)
    except (json.JSONDecodeError, TypeError):
        return _fallback_recommendations(book, top_n)

    candidates = (
        Book.objects.filter(is_deleted=False, is_active=True)
        .exclude(pk=book.pk)
        .exclude(embedding_vector__isnull=True)
        .exclude(embedding_vector="")
        .prefetch_related("authors", "categories")[:100]
    )

    scored = []
    for candidate in candidates:
        try:
            cand_vec = json.loads(candidate.embedding_vector)
            score = cosine_similarity(target_vec, cand_vec)
            scored.append((score, candidate))
        except (json.JSONDecodeError, TypeError):
            continue

    scored.sort(key=lambda x: x[0], reverse=True)
    return [book for _, book in scored[:top_n]]


def _fallback_recommendations(book, top_n=4):
    from books.models import Book

    category_ids = book.categories.values_list("id", flat=True)
    similar = (
        Book.objects.filter(is_deleted=False, is_active=True)
        .exclude(pk=book.pk)
        .filter(categories__in=category_ids)
        .distinct()[:top_n]
    )

    if similar.count() < top_n:
        extra = (
            Book.objects.filter(is_deleted=False, is_active=True)
            .exclude(pk=book.pk)
            .exclude(pk__in=[b.pk for b in similar])
            .order_by("?")[: top_n - similar.count()]
        )
        return list(similar) + list(extra)

    return list(similar)
