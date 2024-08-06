import fitz  # PyMuPDF
import io
from PIL import Image


def extract_images_from_pdf(pdf_path, output_folder):
    # Ouvrir le document PDF
    pdf_document = fitz.open(pdf_path)

    # Parcourir toutes les pages
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        image_list = page.get_images(full=True)

        # Parcourir toutes les images de la page
        for image_index, img in enumerate(image_list, start=1):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]

            # Ouvrir l'image en utilisant PIL
            try:
                image = Image.open(io.BytesIO(image_bytes))
                image_name = f"page_{page_num+1}_img_{image_index}.{image.format.lower()}"
                image_path = f"{output_folder}/{image_name}"

                # Sauvegarder l'image
                image.save(image_path)
                print(f"Image enregistrée : {image_path}")
            except:
                print(f"Image en erreur: page_{page_num+1}_img_{image_index}")

# Exemple d'utilisation
pdf_path = "C:/Users/delem/Downloads/Lemarchand-Paul.pdf"
output_folder = "images"
extract_images_from_pdf(pdf_path, output_folder)
