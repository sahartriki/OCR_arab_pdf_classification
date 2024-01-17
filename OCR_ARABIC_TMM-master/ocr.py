import os
import pytesseract
from PyPDF2 import PdfReader
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.pipeline import make_pipeline

# Fonction pour extraire le texte d'un document PDF
def extract_text_from_pdf(pdf_path):
    text = ''
    pdf_reader = PdfReader(pdf_path)
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

# Chemins vers les documents PDF et leurs labels
pdf_directory = 'docs pdf'
pdf_files = ['Devoir de Synthèse N°2 - Arabe - 1ère AS  (2011-2012) Mr نزيهة جبر.pdf', 'promesse-type-Quintessence.pdf', 'شهادة تقدير رصاصي وبني .pdf']
labels = ['الفرض', 'عــقــد', 'شهادة']

# Extraction du texte et création du jeu de données
data = []
for pdf_file, label in zip(pdf_files, labels):
    pdf_path = os.path.join(pdf_directory, pdf_file)
    text = extract_text_from_pdf(pdf_path)
    data.append((text, label))

# Division du jeu de données en ensembles d'entraînement et de test
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Création du pipeline du modèle
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Entraînement du modèle
X_train, y_train = zip(*train_data)
model.fit(X_train, y_train)

# Prédiction sur l'ensemble de test
X_test, y_test = zip(*test_data)
y_pred = model.predict(X_test)

# Évaluation du modèle
accuracy = metrics.accuracy_score(y_test, y_pred)
print(f"Précision du modèle : {accuracy}")

# Exemple de prédiction sur un nouveau document PDF
new_pdf_path = 'chemin/vers/votre/nouveau_document.pdf'
new_text = extract_text_from_pdf(new_pdf_path)
predicted_label = model.predict([new_text])[0]
print(f"Le document est prédit comme appartenant à la catégorie : {predicted_label}")
