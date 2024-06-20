import spacy
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_information(text):
    name_pattern = re.compile(r'Name: (.+?),')
    date_pattern = re.compile(r'Date: (.+?), Location:')
    location_pattern = re.compile(r'Location: (.+)$')

    name_match = name_pattern.search(text)
    date_match = date_pattern.search(text)
    location_match = location_pattern.search(text)

    name = name_match.group(1).strip() if name_match else None
    date = date_match.group(1).strip() if date_match else None
    location = location_match.group(1).strip() if location_match else None

    if not name:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "ORG" and not name:
                name = ent.text
            elif ent.label_ == "DATE" and not date:
                date = ent.text
            elif ent.label_ == "GPE" and not location:
                location = ent.text

    return [name, date, location]
