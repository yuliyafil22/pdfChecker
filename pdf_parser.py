import pdfplumber
from pyzbar.pyzbar import decode
from PIL import Image

def parse_pdf(pdf_path):
    """
    Извлекает данные из PDF-файла и возвращает их в виде словаря.
    """
    data = {}
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]  # Предполагаем, что данные на первой странице
        text = page.extract_text()

        # Пример извлечения данных (зависит от структуры вашего PDF)
        for line in text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()

    return data

def extract_barcodes(pdf_path):
    """
    Извлекает баркоды из PDF-файла.
    """
    barcodes = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            im = page.to_image().original  # Получаем изображение страницы
            barcodes.extend(decode(im))  # Распознаем баркоды
    return [barcode.data.decode("utf-8") for barcode in barcodes]

def save_reference_data(data, barcodes, output_file="reference_data.txt"):
    """
    Сохраняет эталонные данные и баркоды в файл.
    """
    with open(output_file, "w") as f:
        for key, value in data.items():
            f.write(f"{key}: {value}\n")
        f.write("BARCODES:\n")
        for barcode in barcodes:
            f.write(f"{barcode}\n")

def load_reference_data(input_file="reference_data.txt"):
    """
    Загружает эталонные данные и баркоды из файла.
    """
    data = {}
    barcodes = []
    with open(input_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("BARCODES:"):
                continue
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()
            else:
                barcodes.append(line.strip())
    return data, barcodes

def compare_with_reference(test_data, test_barcodes, reference_data, reference_barcodes):
    """
    Сравнивает данные и баркоды тестового PDF с эталоном и возвращает отклонения.
    """
    discrepancies = {}
    for key in reference_data:
        if key not in test_data:
            discrepancies[key] = "Отсутствует"
        elif test_data[key] != reference_data[key]:
            discrepancies[key] = f"Ожидалось: {reference_data[key]}, Найдено: {test_data[key]}"

    # Проверка баркодов
    if set(test_barcodes) != set(reference_barcodes):
        discrepancies["BARCODES"] = f"Ожидалось: {reference_barcodes}, Найдено: {test_barcodes}"

    return discrepancies