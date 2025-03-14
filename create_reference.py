from pdf_parser import parse_pdf, extract_barcodes, save_reference_data

# Путь к эталонному PDF-файлу
reference_pdf_path = "test_pdfs/reference.pdf"

# Извлекаем данные из эталонного PDF
reference_data = parse_pdf(reference_pdf_path)

# Извлекаем баркоды из эталонного PDF
reference_barcodes = extract_barcodes(reference_pdf_path)

# Сохраняем эталонные данные и баркоды в файл
save_reference_data(reference_data, reference_barcodes)

print("Эталонные данные и баркоды сохранены в reference_data.txt.")