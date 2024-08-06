import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTImage, LTFigure

# Chemin du fichier PDF
# Chemin du fichier PDF
pdf_file = "C:/Users/delem/Downloads/Lemarchand-Paul_calques_on.pdf"
output_dir = "extracted_images"

# Crée le répertoire de sortie si nécessaire
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Fonction pour extraire les images et les objets binaires
def extract_images_from_element(element, page_number):
    if isinstance(element, LTImage):
        save_image(element, page_number)
    elif isinstance(element, LTFigure):
        for fig_element in element:
            extract_images_from_element(fig_element, page_number)

# Fonction pour enregistrer les images extraites
def save_image(lt_image, page_number):
    if lt_image.stream:
        file_stream = lt_image.stream.get_rawdata()
        if file_stream:
            image_filename = f"{output_dir}/image_page_{page_number}_{lt_image.name}.jpg"
            with open(image_filename, "wb") as image_file:
                image_file.write(file_stream)
            print(f"Image saved as: {image_filename}")

# Configuration de PDFMiner
resource_manager = PDFResourceManager()
laparams = LAParams(detect_vertical=True, all_texts=True)
device = PDFPageAggregator(resource_manager, laparams=laparams)
interpreter = PDFPageInterpreter(resource_manager, device)

# Lecture du fichier PDF et extraction des images
with open(pdf_file, 'rb') as file:
    for page_number, page in enumerate(PDFPage.get_pages(file)):
        interpreter.process_page(page)
        layout = device.get_result()
        for element in layout:
            extract_images_from_element(element, page_number)
