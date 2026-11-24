"""Text cleaning and resume file reading. clean_text MUST match the notebook's version."""
import io
import re

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

URL = re.compile(r"https?://\S+|www\.\S+")
EMAIL = re.compile(r"\S+@\S+")
PHONE = re.compile(r"\+?\d[\d\-\s()]{7,}\d")
NON_ALPHA = re.compile(r"[^a-z+#\s]")      # keep + and # so "c++" and "c#" survive


def clean_text(text) -> str:
    """Lowercase; remove URLs, emails, phone numbers (personal identifiers), punctuation, stop words."""
    t = str(text).lower()
    for pat in (URL, EMAIL, PHONE):
        t = pat.sub(" ", t)
    t = NON_ALPHA.sub(" ", t)
    return " ".join(w for w in t.split() if w not in ENGLISH_STOP_WORDS and len(w) > 1)


def extract_text(data: bytes, filename: str) -> str:
    """Read text from an uploaded PDF, DOCX or TXT resume."""
    name = filename.lower()
    if name.endswith(".pdf"):
        from pypdf import PdfReader
        return "\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(data)).pages)
    if name.endswith(".docx"):
        import docx
        return "\n".join(p.text for p in docx.Document(io.BytesIO(data)).paragraphs)
    return data.decode("utf-8", errors="ignore")
