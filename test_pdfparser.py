import os
import pytest
from pdf_parser import parse_pdf, extract_barcodes, load_reference_data, compare_with_reference

# Загружаем эталонные данные один раз для всех тестов
reference_data, reference_barcodes = load_reference_data()

# Указываем папку, где находятся тестовые PDF-файлы
test_pdfs_dir = "test_pdfs"

# Получаем список всех PDF-файлов в папке (кроме reference.pdf)
pdf_files = [f for f in os.listdir(test_pdfs_dir) if f.endswith(".pdf") and f != "reference.pdf"]


# Параметризация: каждый файл будет проверяться как отдельный тест
@pytest.mark.parametrize("pdf_file", pdf_files)
def test_pdf_file(pdf_file):
    """
    Тестирует один PDF-файл на соответствие эталону.

    :param pdf_file: Имя PDF-файла для тестирования.
    """
    # Формируем полный путь к файлу
    pdf_path = os.path.join(test_pdfs_dir, pdf_file)
    print(f"\nТестирование файла: {pdf_file}...")

    # Проверяем, существует ли файл
    if not os.path.exists(pdf_path):
        pytest.fail(f"Файл {pdf_file} не найден в папке test_pdfs.")

    # Извлекаем данные из тестового PDF
    test_data = parse_pdf(pdf_path)

    # Извлекаем баркоды из тестового PDF
    test_barcodes = extract_barcodes(pdf_path)

    # Сравниваем данные и баркоды с эталоном
    discrepancies = compare_with_reference(test_data, test_barcodes, reference_data, reference_barcodes)

    # Если есть отклонения, проваливаем тест и выводим сообщение об ошибке
    if discrepancies:
        error_message = f"Найдены отклонения в файле {pdf_file}:\n"
        for key, value in discrepancies.items():
            error_message += f"  {key}: {value}\n"
        pytest.fail(error_message)  # Проваливаем тест с сообщением об ошибке
    else:
        # Если отклонений нет, выводим сообщение об успешном прохождении
        print(f"Файл {pdf_file} соответствует эталону.")

    # Разделитель для удобства чтения вывода
    print("-" * 40)
