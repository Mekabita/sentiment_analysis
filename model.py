from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
import re

# initialize vader sentiment
analyzer = SentimentIntensityAnalyzer()

# download and intialize stopwords 
# nltk.download("stopwords")
# STOP_WORDS = set(stopwords.words("english"))

def preprocess_text(text):
    # do the preprocessing steps like removing emails, whitespace, numbers and stopwords
    text = text.lower()
    # remove email
    text = re.sub(r"http\S+|www\S+|@\S+|mailto:\S+", "", text)
    # remove punctuation
    text = re.sub(r"[^\w\s]", "", text)
    # remove numbers
    text = re.sub(r"\d+", "", text)
    # remove stopwords
    # text = " ".join(word for word in text.split() if word not in STOP_WORDS)
    text = text.strip()
    return text

# Function where the sentiment score will be calculated using VADER
def find_sentiment(user_message):
    # preprocess user message first
    user_message = preprocess_text(user_message)
    sentiment_scores = analyzer.polarity_scores(user_message)
    compound_score = sentiment_scores["compound"]
    print(sentiment_scores, compound_score)
        # Determine sentiment type
    if compound_score >= 0.05:
        sentiment_type = "Positive"
    elif compound_score <= -0.05:
        sentiment_type = "Negative"
    else:
        sentiment_type = "Neutral"
        

    return sentiment_type, compound_score