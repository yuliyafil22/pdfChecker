from pdf_parser import extract_pdf_info, compare_pdf_structure


def test_extract_pdf_info():
    pdf_info = extract_pdf_info("test_pdfs/test_task.pdf")
    assert isinstance(pdf_info, dict)
    assert "text" in pdf_info
    assert isinstance(pdf_info["text"], str)


def test_compare_pdf_structure():
    result = compare_pdf_structure("test_pdfs/test_task1.pdf", "test_pdfs/test_task2.pdf")
    assert isinstance(result, bool)
