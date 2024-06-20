import spacy
import os

def getDetails(post_list):
    post_event_details = []
    # Load transformer-based spaCy model
    nlp = spacy.load('en_core_web_lg')

    # Load the saved model for testing
    dirname = os.path.dirname(__file__)
    checkpoint_dir = os.path.join(dirname, 'enhanced_event_ner_model')
    nlp = spacy.load(checkpoint_dir)

    # Test with sample texts

    for text in post_list:
        doc = nlp(text)

        title = None
        date = None
        location = None

        for ent in doc.ents:
            if ent.label_ == "TITLE":
                title = ent.text
            elif ent.label_ == "DATE":
                date = ent.text
            elif ent.label_ == "LOCATION":
                location = ent.text

        if not title:
            title = "Not Mentioned"
        if not date:
            date = "Not Mentioned"
        if not location:
            location = "Not Mentioned"

        post_event_details.append({"title": title, "date": date, "location": location})

    return post_event_details
