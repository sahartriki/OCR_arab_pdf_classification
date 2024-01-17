import os
import PyPDF2
from PIL import Image
import pytesseract
import chardet

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


# Fonction pour extraire le texte d'un fichier PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
           # text += page.extract_text()

            #page_text = page.extract_text(encoding='utf-8')
            #text += page_text



             
            
            # Obtient le texte brut à partir du PDF
            raw_text = page.extract_text()
            
            # Détecte l'encodage du texte
            encoding_info = chardet.detect(raw_text.encode())
            detected_encoding = encoding_info['encoding']
            
            # Encode le texte avec l'encodage détecté et le décode en tant que chaîne Unicode
            decoded_text = raw_text.encode(detected_encoding, 'replace').decode(detected_encoding)
            
            text += decoded_text

    return text



def perform_ocr(image_path):
   
    image = Image.open(image_path)
    ocr_result = pytesseract.image_to_string(image, lang='ara')
    return(ocr_result)

    



# Fonction de classification simple (à adapter selon vos besoins)
def classify_document(text):
    # Exemple basique : si le texte contient un mot-clé spécifique, le document est classé comme "Contrat"
    if "عقد" in text:
        return "Contrat"
    elif "شهادة" in text:  # Exemple pour le mot-clé "Certificat"
        return "Certificat"
    else:
        return "Autre"
    

def save_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def classify_and_save(category, content):
    output_folder = os.path.join('output', category)
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, f'{category}_output.txt')
    save_to_file(content, output_file)


# Chemin du fichier PDF à traiter
pdf_path = "docs pdf/promesse-type-Quintessence.pdf"
#pdf_path = "docs pdf/شهادة تقدير رصاصي وبني .pdf"

# Chemin de l'image à traiter
image_path = "contrat.png"
#image_path = "certficats.png"

# Extraction de texte du PDF
pdf_text = extract_text_from_pdf(pdf_path) 

# Perform OCR sur le texte extrait (c'est ici que vous auriez normalement l'image de texte)
ocr_text = perform_ocr(image_path)

# Classification du document
document_category = classify_document(ocr_text)


# Enregistrement des résultats dans des fichiers et organisation par catégorie
pdf_output_file = "pdf_text_output.txt"
image_output_file = "ocr_image_text_output.txt"

save_to_file(pdf_text, pdf_output_file)
save_to_file(ocr_text, image_output_file)

# Classifie et enregistre dans des dossiers spécifiques
if document_category == "Contrat":
    classify_and_save("Contrat", pdf_text)
    classify_and_save("Contrat", ocr_text)
elif document_category == "Certificat":
    classify_and_save("Certificat", pdf_text)
    classify_and_save("Certificat", ocr_text)
else:
    classify_and_save("Autre", pdf_text)
    classify_and_save("Autre", ocr_text)

# Affichage des résultats
print("\n*******************************************\n")
print(f"Texte extrait du PDF : {pdf_text}")
print(f"Résultat de l'OCR sur l'image : {ocr_text}")
print("\n*******************************************\n")
print(f"Catégorie du document : {document_category}")

# Affichage des résultats
print("\n*******************************************\n")
print(f"Texte extrait du PDF : {pdf_text}")
print("\n*******************************************\n")

print(f"Texte après OCR : {ocr_text}")
print("\n*******************************************\n")

print(f"Catégorie du document : {document_category}")

