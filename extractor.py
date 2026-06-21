from __future__ import annotations
from pathlib import Path

from pypdf import PdfReader
from docx import Document
from pptx import Presentation
from openpyxl import load_workbook

def extract_text(path: Path, *, max_chars: int = 2_000) -> str:

    suffix = path.suffix.lower()

    if suffix == ".docx":
        return _extract_docx(path, max_chars=max_chars)
    if suffix == ".txt":
        return _extract_txt(path, max_chars=max_chars)
    if suffix == ".pdf":
        return _extract_pdf(path, max_chars=max_chars)
    if suffix == ".md":
        return _extract_txt(path, max_chars=max_chars)
    if suffix == ".xlsx":
        return _extract_xlsx(path, max_chars=max_chars)
    if suffix == ".pptx":
        return _extract_pptx(path, max_chars=max_chars)
    return ""

def _extract_txt(path: Path, *, max_chars: int) -> str:
    for enc in ("utf-8", "utf-8-sig", "cp1251", "latin-1"):
        try:
            text = path.read_text(encoding=enc, errors="strict")
            return text[:max_chars]
        except UnicodeDecodeError:
            continue
        except OSError:
            return ""

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        return text[:max_chars]
    except OSError:
        return ""

def _extract_docx(path: Path, *, max_chars: int) -> str:
    try:
        doc = Document(str(path))
        parts: list[str] = []
        for para in doc.paragraphs:
                if para.text:
                    parts.append(para.text)
        text = "\n".join(parts)
        return text[:max_chars]
    except Exception:
            return ""

def _extract_pdf(path: Path, *, max_chars: int) -> str:
    try:
        reader = PdfReader(str(path))
        parts: list[str] = []
        total_len = 0
        max_pages = 3
        for page_index, page in enumerate(reader.pages):
            if page_index >= max_pages:
                break
            page_text = page.extract_text() or ""
            page_text = page_text.strip()
            if not page_text:
                continue
            remaining = max_chars - total_len
            if remaining <= 0:
                break
            chunk = page_text[:remaining]
            parts.append(chunk)
            total_len += len(chunk)
            if total_len >= max_chars:
                break
        return "\n".join(parts)
    except Exception:
        return ""

def _extract_pptx(path: Path, *, max_chars: int) -> str:
    try:
        prs = Presentation(str(path))
        parts: list[str] = []
        total_len = 0
        max_slides = 10
        for slide_index, slide in enumerate(prs.slides):
            if slide_index >= max_slides:
                break
            for shape in slide.shapes:
                text = ""
                if hasattr(shape, "text") and shape.text:
                    text = shape.text.strip()
                if not text:
                    continue
                remaining = max_chars - total_len
                if remaining <= 0:
                    return "\n".join(parts)
                chunk = text[:remaining]
                parts.append(chunk)
                total_len += len(chunk)
                if total_len >= max_chars:
                    return "\n".join(parts)
        return "\n".join(parts)
    except Exception:
        return ""

def _extract_xlsx(path: Path, *, max_chars: int) -> str:
    try:
        wb = load_workbook(filename=str(path), read_only=True, data_only=True)
        parts: list[str] = []
        total_len = 0
        max_sheets = 2
        max_rows_per_sheet = 50
        for sheet_index, sheet in enumerate(wb.worksheets):
            if sheet_index >= max_sheets:
                break
            row_count = 0
            for row in sheet.iter_rows(values_only=True):
                if row_count >= max_rows_per_sheet:
                    break
                values = [str(cell).strip() for cell in row if cell is not None and str(cell).strip()]
                if not values:
                    row_count += 1
                    continue
                line = " | ".join(values)
                remaining = max_chars - total_len
                if remaining <= 0:
                    wb.close()
                    return "\n".join(parts)
                chunk = line[:remaining]
                parts.append(chunk)
                total_len += len(chunk)
                if total_len >= max_chars:
                    wb.close()
                    return "\n".join(parts)
                row_count += 1

        wb.close()
        return "\n".join(parts)
    except Exception:
        return ""