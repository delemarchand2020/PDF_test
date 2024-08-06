import fitz  # PyMuPDF


def list_pdf_objects(pdf_path):
    pdf_document = fitz.open(pdf_path)

    # List metadata
    metadata = pdf_document.metadata
    print("Metadata:")
    for key, value in metadata.items():
        print(f"  {key}: {value}")
    print("----")

    # List attachments
    attachments = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        annotations = page.annots()
        if annotations:
            for annot in annotations:
                if annot.type[0] == 8:  # File attachment
                    file_info = annot.file_info
                    attachments.append(file_info)

    print(f"Attachments: {len(attachments)}")
    for attachment in attachments:
        print(f"  {attachment['filename']} - {attachment['desc']}")
    print("----")

    # List layers (Optional Content Groups)
    layers = {}
    for xref in range(1, pdf_document.xref_length()):
        obj = pdf_document.xref_object(xref)
        if "/OCG" in obj or "/OCProperties" in obj:
            layers[xref] = obj

    print(f"Layers (OCGs): {len(layers)}")
    for xref, content in layers.items():
        print(f"Layer {xref}: {content}")
    print("----")

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)

        # List text
        text = page.get_text("text")
        print(f"Page {page_num + 1} Text: {text[:100]}...")

        # Extract text from annotations
        annotations = page.annots()
        if annotations:
            for annot in annotations:
                if annot.info.get("content"):
                    print(f"Page {page_num + 1} Annotation Text: {annot.info.get('content')}")

        # Extract text from form fields
        form_fields = page.widgets()
        if form_fields:
            for field in form_fields:
                if field.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                    print(f"Page {page_num + 1} Form Field Text: {field.text}")

        # List images
        image_list = page.get_images(full=True)
        print(f"Page {page_num + 1} Images: {len(image_list)}")

        # List annotations
        annot_count = sum(1 for _ in annotations) if annotations else 0
        print(f"Page {page_num + 1} Annotations: {annot_count}")

        # List links
        links = page.get_links()
        print(f"Page {page_num + 1} Links: {len(links)}")

        # List form fields
        form_field_count = sum(1 for _ in form_fields) if form_fields else 0
        print(f"Page {page_num + 1} Form Fields: {form_field_count}")

        print("----")

import fitz  # PyMuPDF

def activate_all_layers(pdf_path, output_path):
    # Ouvrir le document PDF
    doc = fitz.open(pdf_path)

    # Parcourir toutes les pages du document
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # Récupérer les annotations de la page
        annotations = page.annots()
        if annotations:
            for annot in annotations:
                # Vérifier si l'annotation est un calque (OCG)
                if annot.type[0] == 8:  # Le type 8 correspond aux OCGs (Optional Content Groups)
                    # Activer l'annotation (calque)
                    annot.set_flags(fitz.ANNOT_VISIBLE)

    # Enregistrer le document modifié
    doc.save(output_path)
    print(f"All layers activated and saved to {output_path}")

# Exemple d'utilisation
input_pdf = "C:/Users/delem/Downloads/Lemarchand-Paul.pdf"
output_pdf = "C:/Users/delem/Downloads/Lemarchand-Paul_calques_on.pdf"
activate_all_layers(input_pdf, output_pdf)


# Exemple d'utilisation
pdf_path = output_pdf
list_pdf_objects(pdf_path)
