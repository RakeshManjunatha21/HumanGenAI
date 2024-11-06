# Import necessary libraries
import streamlit as st
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet as wn
import random
import re
import spacy

# Initialize resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nlp = spacy.load("en_core_web_sm")
nltk.download('punkt')

# Define all helper functions here
def get_synonym(word, pos_tag):
    synsets = wn.synsets(word, pos=pos_tag)
    if synsets:
        synonyms = [lemma.name() for synset in synsets for lemma in synset.lemmas() if lemma.name().lower() != word.lower()]
        if synonyms:
            return random.choice(synonyms).replace('_', ' ')
    return word

def add_filler_words(text):
    filler_words = ['um', 'uh', 'like', 'you know', 'well', 'actually', 'basically', 'honestly']
    sentences = sent_tokenize(text)
    new_sentences = []
    for sentence in sentences:
        if random.random() < 0.15:  
            words = sentence.split()
            insert_pos = random.randint(0, len(words))
            filler = random.choice(filler_words)
            words.insert(insert_pos, filler)
            sentence = ' '.join(words)
        new_sentences.append(sentence)
    return ' '.join(new_sentences)

def vary_contractions(text):
    contractions = {
        "I am": "I'm", "You are": "You're", "He is": "He's", "She is": "She's",
        "It is": "It's", "We are": "We're", "They are": "They're",
        "What is": "What's", "That is": "That's", "Who is": "Who's",
        "Cannot": "Can't", "Do not": "Don't", "Does not": "Doesn't",
        "Did not": "Didn't", "Is not": "Isn't", "Was not": "Wasn't",
        "Were not": "Weren't", "Have not": "Haven't", "Has not": "Hasn't",
        "Had not": "Hadn't", "Will not": "Won't", "Would not": "Wouldn't"
    }
    for full, contraction in contractions.items():
        if random.random() < 0.6:  
            text = re.sub(r'\b' + full + r'\b', contraction, text)
        else:
            text = re.sub(r'\b' + contraction + r'\b', full, text)
    return text

def rewrite_overused_terms(text):
    overused_terms = {
        r'\bin today\'s world\b': ['nowadays', 'in our current times', 'in this day and age'],
        r'\bunlock\b': ['reveal', 'discover', 'access'],
        r'\bcritical\b': ['vital', 'key', 'crucial'],
        r'\bdelve\b': ['explore', 'investigate', 'examine'],
        r'\bin conclusion\b': ['to sum up', 'finally', 'to wrap up'],
        r'\bfurthermore\b': ['also', 'in addition', 'moreover'],
        r'\bbustling\b': ['lively', 'active', 'busy']
    }
    for term, replacements in overused_terms.items():
        text = re.sub(term, lambda m: random.choice(replacements), text, flags=re.IGNORECASE)
    return text

def use_active_voice(text):
    doc = nlp(text)
    active_sentences = []
    for sent in doc.sents:
        if any(token.dep_ == "nsubjpass" for token in sent):
            subject = next((token for token in sent if token.dep_ == "nsubjpass"), None)
            verb = next((token for token in sent if token.dep_ == "auxpass"), None)
            obj = next((token for token in sent if token.dep_ == "dobj"), None)

            if subject and verb and obj:
                active_sent = f"{obj.text.capitalize()} {verb.text} {subject.text}."
                active_sentences.append(active_sent)
            else:
                active_sentences.append(sent.text)
        else:
            active_sentences.append(sent.text)
    return ' '.join(active_sentences)

def add_personal_touch(text):
    personal_touches = [
        "In my experience,",
        "From what I've seen,",
        "I've found that",
        "Personally, I believe",
        "In my opinion,"
    ]
    sentences = sent_tokenize(text)
    for i in range(len(sentences)):
        if random.random() < 0.1: 
            sentences[i] = random.choice(personal_touches) + " " + sentences[i].lower()
    return ' '.join(sentences)

def humanize_text(input_text):
    humanized_text = input_text
    humanized_text = rewrite_overused_terms(humanized_text)
    humanized_text = vary_contractions(humanized_text)
    # humanized_text = add_filler_words(humanized_text)
    humanized_text = use_active_voice(humanized_text)
    # humanized_text = add_personal_touch(humanized_text)

    # Preserve capitalization for "I"
    humanized_text = re.sub(r'\bi\b', 'I', humanized_text)
    humanized_text = re.sub(r'\band\b', lambda m: random.choice(['and', '&']), humanized_text)

    return humanized_text

# Streamlit App Design
st.set_page_config(page_title="AI to Human Text Converter", layout="wide")
st.title("AI to Human Text Converter")
st.markdown("""
""")

# Input and Output Section
input_text = st.text_area("Enter AI-Generated Text", placeholder="Type or paste your text here...", height=200)
if st.button("Convert to Human-Like Text"):
    if input_text.strip():
        with st.spinner("Converting text..."):
            output_text = humanize_text(input_text)
            st.subheader("Human-Like Text Output")
            st.write(output_text)
    else:
        st.error("Please enter some text to convert.")
