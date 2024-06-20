import re
import os
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score, roc_auc_score, roc_curve
from imblearn.over_sampling import SMOTE, ADASYN
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
import nltk
import unicodedata

# Download stopwords and wordnet
nltk.download('stopwords')
nltk.download('wordnet')

# Sample data
from hello import X
y = [1,0,1,0,0,0,1,0,1,1,1,1,1,0,0,0,0,0,0,0,1,0,1,0,1,1,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,0,1,1,1,1,1,1,0,0,0,1,0,0,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,1,1,1,1,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1]

# Text preprocessing function
def preprocess_text(text):
    # Remove emojis and non-alphanumeric characters
    emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"
                            u"\U0001F300-\U0001F5FF"
                            u"\U0001F680-\U0001F6FF"
                            u"\U0001F1E0-\U0001F1FF"
                            u"\U00002500-\U00002BEF"
                            u"\U00002702-\U000027B0"
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            u"\U0001f926-\U0001f937"
                            u"\U00010000-\U0010ffff"
                            u"\u2640-\u2642"
                            u"\u2600-\u2B55"
                            u"\u200d"
                            u"\u23cf"
                            u"\u23e9"
                            u"\u231a"
                            u"\ufe0f"
                            u"\u3030"
                            "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    # Lowercase
    text = text.lower()
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    text = ' '.join([word for word in words if word not in stop_words])
    
    # Lemmatize and Stem
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    text = ' '.join([stemmer.stem(lemmatizer.lemmatize(word)) for word in text.split()])
    
    return text

def normalize_unicode(text):
    normalized_text = unicodedata.normalize('NFKD', text)
    ascii_text = ''.join(c for c in normalized_text if ord(c) < 128)
    return ascii_text

def ppreprocess_text(text):
    normalized_text = normalize_unicode(text)
    lower_text = normalized_text.lower()
    return lower_text

def predict_events(texts):
    optimal_threshold = 0.4755820082695083
    dirname = os.path.dirname(__file__)
    model_file_name = os.path.join(dirname, 'detectIfEventModel/event_detector_model.joblib')
    vectorizer_file_name = os.path.join(dirname, 'detectIfEventModel/tfidf_vectorizer.joblib')
    model = joblib.load(model_file_name)
    vectorizer = joblib.load(vectorizer_file_name)
    texts_preprocessed = [ppreprocess_text(preprocess_text(text)) for text in texts]
    texts_vectorized = vectorizer.transform(texts_preprocessed)
    predictions_proba = model.predict_proba(texts_vectorized)[:, 1]
    predictions = (predictions_proba >= optimal_threshold).astype(int)
    
    return predictions
