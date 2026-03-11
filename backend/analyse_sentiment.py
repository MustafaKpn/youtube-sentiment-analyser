
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from extract_comments import extract_comments
import emoji
import re
import pandas as pd
import os


current_dir = os.getcwd()
df = pd.read_csv(current_dir + "/Emoji_Sentiment_Data_v1.0.csv")

df["compound"] = round((df["Positive"] - df["Negative"]) / df["Occurrences"], 3)
emoji_scores = dict(zip(df["Unicode codepoint"], df["compound"]))


cleanup = re.compile(r'[^\w]')



def is_emoji_only(text: str) -> bool:
    text = emoji.replace_emoji(text, '')
    text = cleanup.sub('', text)
    return len(text.strip()) == 0


def analyse_sentiment(video_data):        
    analyzer = SentimentIntensityAnalyzer()
    comments = video_data['comments']

    for comment in comments:
        text = comment.get('text', '')
        

        if is_emoji_only(text):
            emoji_compound_score = sum([emoji_scores[hex(ord(c))] if c in emoji_scores else 0 for c in text]) / len(text)

            comment['sentiment']= {
                'positive': None,
                'negative': None,
                'neutral': None,
                'compound': emoji_compound_score  # -1 to +1 overall score
                }
            
            continue



        text = emoji.replace_emoji(text, replace='')
        scores = analyzer.polarity_scores(text)
        comment['sentiment'] = {
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'compound': scores['compound'] 
        }

    return video_data


def compute_statistics(video_data):
    """Compute aggregate sentiment statistics"""
    
    comments = video_data['comments']
    
    if not comments:
        return {}
    
    compounds = [c['sentiment']['compound'] for c in comments if c['sentiment'] is not None]
    
    # Classify comments
    positive = [c for c in compounds if c >= 0.05]
    negative = [c for c in compounds if c <= -0.05]
    neutral = [c for c in compounds if -0.05 < c < 0.05]
    
    avg_compound = sum(compounds) / len(compounds)
    
    stats = {
        'total_comments': len(comments),
        'average_sentiment': round(avg_compound, 3),
        'positive_count': len(positive),
        'negative_count': len(negative),
        'neutral_count': len(neutral),
        'positive_percentage': round(len(positive) / len(comments) * 100, 1),
        'negative_percentage': round(len(negative) / len(comments) * 100, 1),
        'neutral_percentage': round(len(neutral) / len(comments) * 100, 1),
    }

    video_data['sentiment_stats'] = stats
    return video_data
