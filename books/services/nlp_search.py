import json
import numpy as np


def encode_query(query_text):
    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
        embedding = model.encode(query_text, convert_to_numpy=True)
        return embedding.tolist()
    except Exception:
        return None


def cosine_similarity(vec_a, vec_b):
    a = np.array(vec_a)
    b = np.array(vec_b)
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    if norm == 0:
        return 0.0
    return float(np.dot(a, b) / norm)


def semantic_search(query, top_n=10, threshold=0.15):
    from books.models import Book

    query_vec = encode_query(query)
    if not query_vec:
        return [], "Could not encode query. sentence-transformers may not be installed."

    candidates = (
        Book.objects.filter(is_deleted=False, is_active=True)
        .exclude(embedding_vector__isnull=True)
        .exclude(embedding_vector="")
        .prefetch_related("authors", "categories")
        .select_related("publisher", "language")
    )

    if not candidates.exists():
        return [], "No book embeddings found. Run: python manage.py generate_embeddings"

    scored = []
    for book in candidates:
        try:
            book_vec = json.loads(book.embedding_vector)
            score = cosine_similarity(query_vec, book_vec)
            if score >= threshold:
                scored.append((score, book))
        except (json.JSONDecodeError, TypeError):
            continue

    scored.sort(key=lambda x: x[0], reverse=True)

    results = []
    for score, book in scored[:top_n]:
        results.append(
            {
                "book": book,
                "score": round(score * 100, 1),
                "relevance": _score_label(score),
            }
        )

    return results, None


def _score_label(score):
    if score >= 0.55:
        return "Very Relevant"
    if score >= 0.40:
        return "Relevant"
    if score >= 0.25:
        return "Somewhat Relevant"
    return "Low Match"


def keyword_fallback(query, top_n=10):
    from books.models import Book
    from django.db.models import Q

    books = (
        Book.objects.filter(is_deleted=False, is_active=True)
        .filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(tags__icontains=query)
            | Q(authors__first_name__icontains=query)
            | Q(authors__last_name__icontains=query)
            | Q(categories__name__icontains=query)
        )
        .distinct()
        .prefetch_related("authors", "categories")
        .select_related("publisher")[:top_n]
    )

    return [{"book": book, "score": None, "relevance": "Keyword Match"} for book in books]


def hybrid_search(query, top_n=10):
    semantic_results, error = semantic_search(query, top_n=top_n)

    if error or not semantic_results:
        keyword_results = keyword_fallback(query, top_n=top_n)
        return keyword_results, "keyword", error

    semantic_ids = {r["book"].pk for r in semantic_results}
    keyword_results = keyword_fallback(query, top_n=top_n)

    for kr in keyword_results:
        if kr["book"].pk not in semantic_ids:
            kr["relevance"] = "Keyword Match"
            semantic_results.append(kr)

    return semantic_results[:top_n], "semantic", None
