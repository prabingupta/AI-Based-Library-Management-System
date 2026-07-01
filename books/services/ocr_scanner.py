import cv2
import numpy as np
import pytesseract
import re
from PIL import Image


def preprocess_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        return None, "Could not decode image."

    h, w = img.shape[:2]
    if max(h, w) > 2000:
        scale = 2000 / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    denoised = cv2.fastNlMeansDenoising(gray, h=10)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)

    _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh, None


def extract_text_from_image(image_bytes):
    processed, error = preprocess_image(image_bytes)
    if error:
        return None, error

    pil_img = Image.fromarray(processed)

    configs = [
        "--oem 3 --psm 6",
        "--oem 3 --psm 4",
        "--oem 3 --psm 3",
    ]

    best_text = ""
    for config in configs:
        try:
            text = pytesseract.image_to_string(pil_img, config=config)
            if len(text.strip()) > len(best_text.strip()):
                best_text = text
        except Exception:
            continue

    if not best_text.strip():
        return None, "No text could be extracted from this image."

    return best_text.strip(), None


def parse_book_info(raw_text):
    lines = [line.strip() for line in raw_text.split("\n") if line.strip() and len(line.strip()) > 2]

    candidates = []
    for line in lines:
        cleaned = re.sub(r"[^a-zA-Z0-9\s\-:',.]", "", line).strip()
        if len(cleaned) > 4:
            candidates.append(cleaned)

    isbn_pattern = re.compile(r"\b(?:97[89][-\s]?)?(?:\d[-\s]?){9}[\dXx]\b")
    isbns = []
    for line in lines:
        found = isbn_pattern.findall(line)
        for isbn in found:
            clean_isbn = re.sub(r"[-\s]", "", isbn)
            if len(clean_isbn) in [10, 13]:
                isbns.append(clean_isbn)

    title_candidates = []
    author_candidates = []

    author_keywords = ["by ", "author:", "written by", "edited by"]
    for line in candidates:
        lower = line.lower()
        is_author = any(kw in lower for kw in author_keywords)
        if is_author:
            for kw in author_keywords:
                if kw in lower:
                    author_part = line[lower.index(kw) + len(kw) :].strip()
                    if author_part:
                        author_candidates.append(author_part)
        else:
            words = line.split()
            if 2 <= len(words) <= 12:
                title_candidates.append(line)

    title = title_candidates[0] if title_candidates else ""
    possible_author = author_candidates[0] if author_candidates else ""

    return {
        "title_candidates": title_candidates[:5],
        "author_candidates": author_candidates[:3],
        "isbns": isbns[:3],
        "best_title": title,
        "best_author": possible_author,
        "raw_lines": candidates[:20],
    }


def scan_book_cover(image_bytes):
    raw_text, error = extract_text_from_image(image_bytes)
    if error:
        return None, error

    parsed = parse_book_info(raw_text)
    parsed["raw_text"] = raw_text

    search_results = []

    if parsed["isbns"]:
        from books.services.isbn_lookup import lookup_isbn

        for isbn in parsed["isbns"][:2]:
            data, err = lookup_isbn(isbn)
            if data:
                data["match_type"] = "isbn"
                search_results.append(data)

    if not search_results and parsed["title_candidates"]:
        from books.services.isbn_lookup import _search_by_title

        for title in parsed["title_candidates"][:3]:
            results = _search_by_title(title)
            if results:
                for r in results[:2]:
                    r["match_type"] = "title"
                    search_results.append(r)
                break

    return {
        "ocr_data": parsed,
        "search_results": search_results[:4],
        "raw_text": raw_text,
    }, None
