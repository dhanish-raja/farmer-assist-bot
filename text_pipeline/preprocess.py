import re
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


nlp = spacy.load("en_core_web_sm")
STOP_WORDS = set(stopwords.words("english"))

BAD_TOKENS = {
    "im","ive","ill","id","youre","dont","cant","wont",
    "isnt","arent","wasnt","werent","havent","hasnt",
    "hadnt","doesnt","didnt","shouldnt","wouldnt","couldnt"
}

def normalize(text):
    text = text.lower()
    text = re.sub(r"[’']", "", text)
    return text.strip()

def remove_noise(text):
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+\.\S+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def clean_tokens(tokens):
    return [
        t.lower() for t in tokens
        if t.lower() not in STOP_WORDS
        and t.lower() not in BAD_TOKENS
        and len(t) > 2
        and t.isalpha()
    ]

def lemmatize(tokens):
    doc = nlp(" ".join(tokens))
    return [t.lemma_ for t in doc]

def preprocess(text):
    text = normalize(text)
    text = remove_noise(text)
    tokens = word_tokenize(text)
    tokens = clean_tokens(tokens)
    tokens = lemmatize(tokens)
    return tokens

