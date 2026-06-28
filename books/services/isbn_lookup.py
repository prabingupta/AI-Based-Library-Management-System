import re
import urllib.request
import urllib.error
import json

OPEN_LIBRARY_URL = "https://openlibrary.org/api/books"
OPEN_LIBRARY_SEARCH = "https://openlibrary.org/search.json"


def lookup_isbn(isbn):
    isbn = isbn.strip().replace("-", "").replace(" ", "")
    if not isbn:
        return None, "ISBN is required."

    data = _fetch_by_isbn(isbn)
    if data:
        return data, None

    data = _fetch_by_search(isbn)
    if data:
        return data, None

    return None, f"No book found for ISBN: {isbn}"


def _parse_year(pub_date):
    if not pub_date:
        return None
    years = re.findall(r"\b((?:19|20)\d{2})\b", str(pub_date))
    if years:
        return int(years[0])
    return None


def _parse_authors(raw_authors):
    authors = []
    for a in raw_authors:
        name = a.get("name", "") if isinstance(a, dict) else str(a)
        name = name.strip()
        if not name:
            continue
        parts = name.split()
        if len(parts) >= 2:
            authors.append({"first_name": parts[0], "last_name": " ".join(parts[1:])})
        else:
            authors.append({"first_name": name, "last_name": ""})
    return authors


def _fetch_by_isbn(isbn):
    try:
        bibkey = f"ISBN:{isbn}"
        url = f"{OPEN_LIBRARY_URL}?bibkeys={bibkey}&format=json&jscmd=data"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "LibraryOS/1.0 (library management system)"},
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            raw = json.loads(response.read().decode())

        book_data = raw.get(bibkey)
        if not book_data:
            return None

        return _parse_isbn_response(isbn, book_data)

    except (urllib.error.URLError, json.JSONDecodeError, Exception):
        return None


def _parse_isbn_response(isbn, data):
    authors = _parse_authors(data.get("authors", []))

    publishers = data.get("publishers", [])
    publisher = publishers[0].get("name", "") if publishers else ""

    covers = data.get("cover", {})
    cover_url = covers.get("large") or covers.get("medium") or covers.get("small", "")

    pub_year = _parse_year(data.get("publish_date", ""))

    subjects = data.get("subjects", [])
    categories = []
    for s in subjects[:5]:
        name = s.get("name", "") if isinstance(s, dict) else str(s)
        if name:
            categories.append(name)

    description = data.get("description", "")
    if isinstance(description, dict):
        description = description.get("value", "")

    return {
        "title": data.get("title", ""),
        "isbn": isbn if len(isbn) == 10 else "",
        "isbn13": isbn if len(isbn) == 13 else "",
        "authors": authors,
        "publisher": publisher,
        "description": str(description)[:500] if description else "",
        "pages": data.get("number_of_pages"),
        "publication_year": pub_year,
        "cover_url": cover_url,
        "categories": categories,
        "source": "Open Library",
    }


def _fetch_by_search(isbn):
    try:
        url = f"{OPEN_LIBRARY_SEARCH}?isbn={isbn}&limit=1"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "LibraryOS/1.0 (library management system)"},
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            raw = json.loads(response.read().decode())

        docs = raw.get("docs", [])
        if not docs:
            return None

        doc = docs[0]

        authors = []
        for name in doc.get("author_name", [])[:3]:
            parts = name.strip().split()
            if len(parts) >= 2:
                authors.append({"first_name": parts[0], "last_name": " ".join(parts[1:])})
            else:
                authors.append({"first_name": name, "last_name": ""})

        publishers = doc.get("publisher", [])
        publisher = publishers[0] if publishers else ""

        pub_years = doc.get("publish_year", [])
        pub_year = max(pub_years) if pub_years else None

        return {
            "title": doc.get("title", ""),
            "isbn": isbn if len(isbn) == 10 else "",
            "isbn13": isbn if len(isbn) == 13 else "",
            "authors": authors,
            "publisher": publisher,
            "description": "",
            "pages": doc.get("number_of_pages_median"),
            "publication_year": pub_year,
            "cover_url": "",
            "categories": doc.get("subject", [])[:5],
            "source": "Open Library Search",
        }

    except (urllib.error.URLError, json.JSONDecodeError, Exception):
        return None
