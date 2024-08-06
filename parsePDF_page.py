
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import (LAParams, LTTextBox, LTTextLine, LTFigure, LTText, LTTextContainer, LTChar, LTTextGroup,
                             LTImage, LTCurve, LTAnno)

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBox, LTTextLine, LTChar, LTAnno, LTFigure, LTImage, LTRect, LTCurve
import pandas as pd
output = []
def parse_layout(layout):
    """Function to recursively parse the layout tree."""

    for lt_obj in layout:

        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine) or isinstance(lt_obj, LTText)\
                or isinstance(lt_obj, LTTextContainer) or isinstance(lt_obj, LTChar) or isinstance(lt_obj, LTTextGroup)\
                or isinstance(lt_obj, LTAnno):
            output.append([lt_obj.__class__.__name__, lt_obj.get_text()])
        elif isinstance(lt_obj, LTFigure):
            parse_layout(lt_obj)  # Recursive
        elif not isinstance(lt_obj, LTImage) and not isinstance(lt_obj, LTCurve):
            parse_layout(lt_obj)
        else:
            output.append([lt_obj.__class__.__name__,"no text"])

pdf_path = ("C:/Users/delem/Downloads/Lemarchand-Paul_calques_on.pdf")

with open(pdf_path, "rb") as f:
    parser = PDFParser(f)
    doc = PDFDocument(parser)
    page = list(PDFPage.create_pages(doc))[7]  # Page Number
    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=LAParams(all_texts=True))
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    interpreter.process_page(page)
    layout = device.get_result()
    _, _, width, height = page.mediabox
    parse_layout(layout)

#output = pd.DataFrame(output, columns=["bbox_type", "coords", "token"])
#output[["word_xMin", "word_yMin", "word_xMax", "word_yMax"]] =  output["coords"].to_list()

#print(output)



# Chemin du fichier PDF
pdf_file = pdf_path

# Fonction pour extraire le texte de différents éléments
def extract_text_from_element(element):
    text = ""
    try:
        text += element.get_text()
    except:
        try:
            for fig_element in element:
                text += extract_text_from_element(fig_element)
        except:
            pass
    return text

# Configuration de PDFMiner
resource_manager = PDFResourceManager()
laparams = LAParams(detect_vertical=True, all_texts=True)
device = PDFPageAggregator(resource_manager, laparams=laparams)
interpreter = PDFPageInterpreter(resource_manager, device)

page_num = 6
# Lecture du fichier PDF
with open(pdf_file, 'rb') as file:
    for i, page in enumerate(PDFPage.get_pages(file)):
        if i != page_num:
            continue
        interpreter.process_page(page)
        layout = device.get_result()
        page_text = ""
        for element in layout:
            page_text += extract_text_from_element(element)
        print(f'-----------------Texte extrait de la page {i} ----------------------------------\n {page_text}')