import google.generativeai as genai
from django.conf import settings


def get_library_context():
    from books.models import Book, Category
    from members.models import Member
    from borrowing.models import BorrowRecord

    total_books = Book.objects.filter(is_deleted=False).count()
    available = Book.objects.filter(is_deleted=False, status="available").count()
    total_members = Member.objects.filter(is_deleted=False).count()
    active_borrows = BorrowRecord.objects.filter(status__in=["borrowed", "renewed"]).count()

    categories = list(Category.objects.filter(is_active=True).values_list("name", flat=True))

    books = Book.objects.filter(is_deleted=False, is_active=True).prefetch_related("authors", "categories")[:30]

    book_list = []
    for book in books:
        authors = ", ".join(a.full_name for a in book.authors.all())
        cats = ", ".join(c.name for c in book.categories.all())
        status = book.status
        copies = book.available_copies
        book_list.append(
            f"- {book.title} by {authors or 'Unknown'} " f"[{cats}] Status: {status}, Available copies: {copies}"
        )

    return f"""
You are LibraryOS Assistant, an AI chatbot for a library management system.

LIBRARY STATISTICS:
- Total books in library: {total_books}
- Available books: {available}
- Total members: {total_members}
- Currently borrowed: {active_borrows}

BOOK CATEGORIES AVAILABLE: {', '.join(categories)}

BOOKS IN LIBRARY:
{chr(10).join(book_list)}

INSTRUCTIONS:
- Answer questions about books, availability, borrowing, fines, and library services.
- Be helpful, friendly, and concise.
- If asked about a specific book, check the list above.
- For questions you cannot answer from this context, suggest contacting the librarian.
- Keep responses under 150 words unless detailed explanation is needed.
- Do not make up book titles or information not in the list above.
""".strip()


def chat_with_gemini(user_message, chat_history=None):
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return "Gemini API key not configured. Please contact your administrator."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        library_context = get_library_context()

        history = []
        if chat_history:
            for msg in chat_history[-6:]:
                role = "user" if msg["role"] == "user" else "model"
                history.append({"role": role, "parts": [msg["content"]]})

        chat = model.start_chat(history=history)

        full_message = f"{library_context}\n\nUser question: {user_message}"
        if history:
            full_message = user_message

        response = chat.send_message(full_message)
        return response.text

    except Exception as e:
        error_msg = str(e).lower()
        if "quota" in error_msg or "limit" in error_msg:
            return "I'm currently experiencing high demand. Please try again in a moment."
        if "api_key" in error_msg or "invalid" in error_msg:
            return "API configuration error. Please contact your administrator."
        return "I'm having trouble connecting right now. Please try again or ask a librarian."
