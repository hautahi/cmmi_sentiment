"""
This program defines a bunch of sentiment analysis functions to be called from other files
"""

# Load packages
import time
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk import sent_tokenize, word_tokenize, pos_tag
import pandas as pd
import re
from nltk.tokenize import WordPunctTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2 import service_account

# ----------------------
# Define Functions
# ----------------------

def clean_text(tweet):
    user_removed = re.sub(r'@[A-Za-z0-9]+','',tweet)
    link_removed = re.sub('https?://[A-Za-z0-9./]+','',user_removed)
    number_removed = re.sub('[^a-zA-Z]', ' ', link_removed)
    lower_case_tweet= number_removed.lower()
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_tweet)
    clean_tweet = (' '.join(words)).strip()
    return(clean_tweet)
 
def penn_to_wn(tag):
    """
    Convert between the PennTreebank tags to simple Wordnet tags
    """
    if tag.startswith('J'):
        return(wn.ADJ)
    elif tag.startswith('N'):
        return(wn.NOUN)
    elif tag.startswith('R'):
        return(wn.ADV)
    elif tag.startswith('V'):
        return(wn.VERB)
    return(None)

def swn_polarity(text):
    """
    Return a sentiment polarity: 0 = negative, 1 = positive
    """
    
    sentiment, tokens_count = 0.0, 0
 
    text = clean_text(text)
  
    raw_sentences = sent_tokenize(text)
    
    # Create lemmatizer instance
    lemmatizer = WordNetLemmatizer()

    for raw_sentence in raw_sentences:
        
        # Tag each word as a part of speech
        tagged_sentence = pos_tag(word_tokenize(raw_sentence))
 
        for word, tag in tagged_sentence:
        
            # Exit loop if word isn't a noun, adjective or adverb
            wn_tag = penn_to_wn(tag)
            if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
                continue
 
            # Exit loop if word can't be lemmatized
            lemma = lemmatizer.lemmatize(word, pos=wn_tag)
            if not lemma:
                continue
            
            # Get synsets and exit if one isn't available
            synsets = wn.synsets(lemma, pos=wn_tag)
            if not synsets:
                continue
 
            # Take the most common sense
            synset = synsets[0]
            swn_synset = swn.senti_synset(synset.name())
             
            # Add to sentiment score
            sentiment += swn_synset.pos_score() - swn_synset.neg_score()
            tokens_count += 1
 
    # judgment call ? Default to positive or negative
    if not tokens_count:
        return(0)
 
    return(sentiment)

def vader_polarity(text):
    
    vader = SentimentIntensityAnalyzer()

    text = clean_text(text)

    score = vader.polarity_scores(text)
    
    return(score['compound'])

def get_sentiment_score(tweet):
    credentials = service_account.Credentials.from_service_account_file('mycreds.JSON',)
    client = language.LanguageServiceClient(credentials=credentials)
    document = types.Document(content=tweet,type=enums.Document.Type.PLAIN_TEXT)
    sentiment_score = client\
                      .analyze_sentiment(document=document)\
                      .document_sentiment\
                      .score
    return(sentiment_score)

