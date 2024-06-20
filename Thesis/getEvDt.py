from groq import Groq
from transformers import pipeline
from getPrmt import getCatPr, getDetPr, getEvPr
from removeLinksAndHashtags import remove_links_and_hashtags
from transformers import BertTokenizer, BertForSequenceClassification

import warnings
import os
import spacy
import torch
import joblib


def getCategories(post_list: list) -> list:
    extracted_posts = [remove_links_and_hashtags(item) for item in post_list]

    dirname = os.path.dirname(__file__)
    checkpoint_dir = os.path.join(dirname, 'results/checkpoint-1640')

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    model = BertForSequenceClassification.from_pretrained(checkpoint_dir)

    pkl_dir = os.path.join(dirname, 'mlb_classes.pkl')
    mlb = joblib.load(pkl_dir)

    # Function to classify new paragraphs
    def classify_paragraph(paragraph):
        encoding = tokenizer.encode_plus(
            paragraph,
            add_special_tokens=True,
            max_length=256,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        input_ids = encoding['input_ids']
        attention_mask = encoding['attention_mask']
        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        predictions = torch.sigmoid(logits).detach().cpu().numpy()
        predicted_labels = mlb.inverse_transform(predictions > 0.5)
        return predicted_labels[0]

    text_with_categories = []
    for item in extracted_posts:
        category = classify_paragraph(item)
        new_dictionary = {item : category}
        text_with_categories.append(new_dictionary)

    return text_with_categories

def get_category(text: str) -> list:
    defined_categories = [
        "Celebration",
        "Software Engineering",
        "Information Technology",
        "Data Science",
        "Computer Science",
        "Conference",
        "Reviews and Study Session",
        "Professional Development",
        "Online Event",
        "Competitions",
        "Guest Speakers",
        "Hackathon",
        "Workshops and Training",
        "Tech Fair",
        "Gaming",
        "Creativity and Artistry",
        "Performing Arts and Talents",
        "Computer Engineering",
        "Spiritual"
    ]
    
    client = Groq(api_key="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")
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": f'''
                {text}

                {getCatPr()}
                '''
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    result = []
    for chunk in completion:
        result.append(chunk.choices[0].delta.content or "")
    
    categories = ''.join(result)
    categories = categories.split(", ")

    return_category = []
    for category in categories:
        if category in defined_categories:
            return_category.append(category)

    return return_category

def det_ev(text: str) -> int:
    
    client = Groq(api_key="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")
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": f'''
                {text}

                {getEvPr()}
                '''
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    result = ""
    for chunk in completion:
        result += chunk.choices[0].delta.content or ""

    return result

def get_dtls(text: str) -> str:
    client = Groq(api_key="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")
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": f'''
                {text}
                
                {getDetPr()}

                '''
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    result = []
    for chunk in completion:
        result.append(chunk.choices[0].delta.content or "")
    
    Details = ''.join(result)
    return Details

def chunk_text(text: str, max_chunk_size=512) -> list:
    # Split the text into chunks of max_chunk_size tokens
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    chunks = []
    current_chunk = []
    current_chunk_size = 0

    for sent in doc.sents:
        sent_length = len(sent)
        if current_chunk_size + sent_length > max_chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_chunk_size = 0

        current_chunk.append(sent.text)
        current_chunk_size += sent_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def summarize(text: str) -> str:
    # Load the summarization pipeline
    summarizer = pipeline("summarization", model="t5-large")
    warnings.filterwarnings("ignore")

    # Split the text into smaller chunks
    chunks = chunk_text(text)

    # Summarize each chunk individually
    summaries = []
    for chunk in chunks:
        # Dynamically adjust max_length and min_length based on chunk size
        chunk_length = len(chunk.split())
        max_length = max(80, chunk_length)
        min_length = min(30, chunk_length // 2)
        
        summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
        summaries.append(summary[0]['summary_text'])

    # Combine the individual summaries
    combined_summary = " ".join(summaries)
    return combined_summary

