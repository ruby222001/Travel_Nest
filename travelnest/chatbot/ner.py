# chatbot/ner.py

import spacy

# Load the spaCy English NER model
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    # Process the text with spaCy NER model
    doc = nlp(text)

    # Extract named entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    return entities
