import cv2
import numpy as np
import pytesseract
import re
from PIL import Image


def preprocess_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        return [], "Could not decode image."

    h, w = img.shape[:2]
    if max(h, w) > 2400:
        scale = 2400 / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))

    variants = []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    variants.append(("gray", gray))

    upscaled = cv2.resize(gray, (gray.shape[1] * 2, gray.shape[0] * 2), interpolation=cv2.INTER_CUBIC)
    variants.append(("upscaled", upscaled))

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    variants.append(("clahe", enhanced))

    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    variants.append(("otsu", otsu))

    _, otsu_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    variants.append(("otsu_inv", otsu_inv))

    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh_blur = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    variants.append(("blur_otsu", thresh_blur))

    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(gray, -1, kernel)
    variants.append(("sharpened", sharpened))

    return variants, None


def extract_text_from_image(image_bytes):
    variants, error = preprocess_image(image_bytes)
    if error:
        return None, error

    configs = [
        "--oem 3 --psm 6",
        "--oem 3 --psm 4",
        "--oem 3 --psm 3",
        "--oem 3 --psm 11",
        "--oem 1 --psm 6",
    ]

    all_texts = set()
    best_text = ""

    for name, variant in variants:
        pil_img = Image.fromarray(variant)
        for config in configs:
            try:
                text = pytesseract.image_to_string(pil_img, config=config)
                cleaned = text.strip()
                if len(cleaned) > len(best_text):
                    best_text = cleaned
                for line in cleaned.split("\n"):
                    line = line.strip()
                    if len(line) > 2:
                        all_texts.add(line)
            except Exception:
                continue

    if not best_text.strip() and not all_texts:
        return None, "No text could be extracted. Try a clearer photo with better lighting."

    combined = best_text if best_text else "\n".join(all_texts)
    return combined.strip(), None


def parse_book_info(raw_text):
    lines = []
    for line in raw_text.split("\n"):
        line = line.strip()
        if len(line) > 2:
            lines.append(line)

    candidates = []
    for line in lines:
        cleaned = re.sub(r"[^a-zA-Z0-9\s\-:',.]", " ", line).strip()
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        if len(cleaned) > 3:
            candidates.append(cleaned)

    isbn_pattern = re.compile(r"\b(?:97[89])[-\s]?(?:\d[-\s]?){9}\d\b|\b\d{9}[\dXx]\b")
    isbns = []
    for line in lines:
        found = isbn_pattern.findall(line)
        for isbn in found:
            clean_isbn = re.sub(r"[-\s]", "", isbn)
            if len(clean_isbn) in [10, 13]:
                isbns.append(clean_isbn)

    author_keywords = ["by ", "author:", "written by", "edited by"]
    title_candidates = []
    author_candidates = []

    for line in candidates:
        lower = line.lower()
        is_author = any(kw in lower for kw in author_keywords)
        if is_author:
            for kw in author_keywords:
                if kw in lower:
                    part = line[lower.index(kw) + len(kw) :].strip()
                    if part:
                        author_candidates.append(part)
        else:
            words = line.split()
            if 2 <= len(words) <= 15 and not line.isdigit():
                title_candidates.append(line)

    return {
        "title_candidates": title_candidates[:6],
        "author_candidates": author_candidates[:3],
        "isbns": isbns[:3],
        "best_title": title_candidates[0] if title_candidates else "",
        "best_author": author_candidates[0] if author_candidates else "",
        "raw_lines": candidates[:25],
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

        for title in parsed["title_candidates"][:4]:
            if len(title.split()) >= 2:
                results = _search_by_title(title)
                if results:
                    for r in results[:2]:
                        r["match_type"] = "title"
                        search_results.append(r)
                    if search_results:
                        break

    seen_titles = set()
    unique_results = []
    for r in search_results:
        t = r.get("title", "").lower().strip()
        if t and t not in seen_titles:
            seen_titles.add(t)
            unique_results.append(r)

    return {
        "ocr_data": parsed,
        "search_results": unique_results[:4],
        "raw_text": raw_text,
    }, None
