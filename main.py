import streamlit as st
import spacy
from nltk.corpus import wordnet as wn
import random
import re

# Load spaCy's English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Helper function to convert spaCy POS tags to WordNet POS tags
def spacy_to_wordnet_pos(spacy_pos):
    """Converts spaCy POS tags to WordNet POS tags."""
    if spacy_pos.startswith('V'):
        return wn.VERB  # Verb
    elif spacy_pos.startswith('N'):
        return wn.NOUN  # Noun
    elif spacy_pos.startswith('J'):
        return wn.ADJ   # Adjective
    elif spacy_pos.startswith('R'):
        return wn.ADV   # Adverb
    else:
        return None

def get_synonyms(word, pos):
    """Retrieve a list of synonyms for a given word and part of speech."""
    # Convert the spaCy POS tag to WordNet POS tag
    wordnet_pos = spacy_to_wordnet_pos(pos)
    if wordnet_pos:
        synsets = wn.synsets(word, pos=wordnet_pos)
        if synsets:
            # Gather synonyms from all synsets
            synonyms = []
            for syn in synsets:
                for lemma in syn.lemmas():
                    if lemma.name().lower() != word.lower():
                        synonyms.append(lemma.name().replace('_', ' '))
            return list(set(synonyms))  # Remove duplicates
    return [word]

def replace_with_synonyms(text, pos):
    """Replace words in the text with synonyms for a more varied vocabulary."""
    doc = nlp(text)
    modified_text = []
    for token in doc:
        if token.pos_ == pos:
            synonyms = get_synonyms(token.text, pos)
            if synonyms:
                modified_text.append(random.choice(synonyms))
            else:
                modified_text.append(token.text)
        else:
            modified_text.append(token.text)
    return " ".join(modified_text)

def add_filler_words(text):
    """Add filler words to make the text sound more conversational and human-like."""
    filler_words = ["like", "you know", "actually"]
    sentences = text.split(". ")
    humanized_sentences = []
    for sentence in sentences:
        if random.random() < 0.5:  # Adjust probability to control filler frequency
            words = sentence.split()
            insert_pos = random.randint(0, len(words) - 1)
            words.insert(insert_pos, random.choice(filler_words))
            sentence = " ".join(words)
        humanized_sentences.append(sentence)
    return ". ".join(humanized_sentences)

def vary_contractions(text):
    """Convert formal phrases to contractions for a more casual tone."""
    contractions = {
        "I am": "I'm", "You are": "You're", "He is": "He's", "She is": "She's",
        "It is": "It's", "We are": "We're", "They are": "They're",
        "What is": "What's", "Cannot": "Can't", "Do not": "Don't"
    }
    for full, contraction in contractions.items():
        text = re.sub(r'\b' + full + r'\b', contraction, text)
    return text

def humanize_text(input_text):
    """Convert AI-generated text into more natural, human-like text."""
    # Replace verbs, nouns, and adjectives with synonyms
    text_with_verbs = replace_with_synonyms(input_text, pos="VERB")
    text_with_nouns = replace_with_synonyms(text_with_verbs, pos="NOUN")
    text_with_adjectives = replace_with_synonyms(text_with_nouns, pos="ADJ")
    
    # Add conversational fillers and contractions
    text_with_fillers = add_filler_words(text_with_adjectives)
    humanized_text = vary_contractions(text_with_fillers)
    return humanized_text

# Streamlit App Design
st.set_page_config(page_title="AI to Human Text Converter", layout="wide")
st.title("AI to Human Text Converter")

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
