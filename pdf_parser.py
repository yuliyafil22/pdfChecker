import pypdf
from typing import Dict


def extract_pdf_info(file_path: str) -> Dict[str, str]:
    """Читает информацию из PDF и возвращает ее в виде словаряя."""
    with open(file_path, "rb") as file:
        reader = pypdf.PdfReader(file)
        metadata = reader.metadata
        text = "".join([page.extract_text() or "" for page in reader.pages])

    return {
        "title": metadata.title if metadata else "",
        "author": metadata.author if metadata else "",
        "text": text.strip()
    }


def compare_pdf_structure(reference_file: str, test_file: str) -> bool:
    """Сравнивает структуру тестируемого PDF с эталонным."""
    ref_info = extract_pdf_info(reference_file)
    test_info = extract_pdf_info(test_file)

    return ref_info["text"] == test_info["text"]
