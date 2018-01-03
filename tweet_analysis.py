
import sys
import time
import json
from collections import Counter
from collections import defaultdict

# Word frequency analysis

def get_hashtags(tweet):
    """Get all hastags from a Tweet.

    Instead of using tweet['entities'], for example,
    we use get() which will not raise a KeyError if
    said field is not present.

    Return: list(hashtags)
    """
    entities = tweet.get('entities', {})
    hastags = entities.get('hashtags', [])
    return [hashtag['text'].lower() for hashtag in hastags]


def get_mentions(tweet):
    """Get all user mentions from a Tweet.

    Return: list(mentions)
    """
    entities = tweet.get('entities', {})
    mentions = entities.get('user_mentions', [])
    return [mention['screen_name'] for mention in mentions]


# Load json file with #User's tweets
fname = 'usr_timeline_realDonaldTrump.jsonl'


# How many tweets contained a 'hashtag'?
with open(fname, 'r') as f:
    hashtagCount = defaultdict(int)
    for line in f:
        tweet = json.loads(line)
        tweetHashtags = get_hashtags(tweet)
        numHashtags = len(tweetHashtags)

        hashtagCount[numHashtags] += 1

    tweets_Hashtags = sum([count for numTags, count in hashtagCount.items() if numTags > 0])
    tweets_noHashtags = hashtagCount[0]
    tweetsTotal = tweets_Hashtags + tweets_noHashtags

    print('Out of {0} tweets total, {1:.3f} % of the tweets had at least 1 hashtag.'.format(
        tweetsTotal, tweets_Hashtags / tweetsTotal))


# How many tweets contained a mention of another user?
with open(fname, 'r') as f:
    mentionCount = defaultdict(int)
    for line in f:
        tweet = json.loads(line)
        tweetmentions = get_mentions(tweet)
        nummentions = len(tweetmentions)

        mentionCount[nummentions] += 1

    tweets_Mentions = sum([count for numMentions, count in mentionCount.items() if numMentions > 0])
    tweets_noMentions = mentionCount[0]
    tweetsTotal = tweets_Mentions + tweets_noMentions

    print('Out of {0} tweets total, {1:.3f} % of the tweets had at least 1 mention.'.format(
        tweetsTotal, tweets_Mentions / tweetsTotal))


# Most common hashtags and mentions
# What are the top 20 most common mentions and hashtags?
with open(fname, 'r') as f:
    hashtags = Counter()
    for line in f:
        tweet = json.loads(line)
        tweetHashtags = get_hashtags(tweet)
        hashtags.update(tweetHashtags)
for hashtag, count in hashtags.most_common(20):
    print('{0:5}   ---   {1:20}'.format(count, hashtag))

with open(fname, 'r') as f:
    mentions = Counter()
    for line in f:
        tweet = json.loads(line)
        tweetmentions = get_mentions(tweet)
        mentions.update(tweetmentions)
for mention, count in mentions.most_common(20):
    print('{0:5}   ---   {1:20}'.format(count, mention))





# Text analysis
import string

# Make sure to download the NLTK corpora first
#import nltk
#nltk.download()  # select multiple corpora in GUI or
#nltk.download("stopwords")   # download a specific one
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords


def process(text, tokenizer=TweetTokenizer(), stopwords=[]):
    """Process the text of a tweet:
    -Lowercase
    -Tokenize
    -Stopword removal
    -Digits removal

    Return: list(strings)
    """
    text = text.lower()
    tokens = tokenizer.tokenize(text)
    tokens = normalize_contractions(tokens)
    return [token for token in tokens if token not in stopwords and not token.isdigit()]


def normalize_contractions(tokens):
    """Normalize english contractions.

    Return: generator
    """
    token_map = {
        "i'm": "i am",
        "you're": "you are",
        "it's": "it is",
        "we'll": "we will",
    }
    for token in tokens:
        if token in token_map.keys():
            for item in token_map[token].split():
                yield item
        else:
            yield token


tweet_tokenizer = TweetTokenizer()

punct = list(string.punctuation)
stopword_list = stopwords.words('english') + punct + ['rt', 'via', '...', '…']

twit = Counter()
with open(fname, 'r') as f:
    for line in f:
        tweet = json.loads(line)
        tokens = process(text=tweet['text'],
                         tokenizer=tweet_tokenizer,
                         stopwords=stopword_list)
        twit.update(tokens)

for token, count in twit.most_common(50):
    print('{0:5}   ---   {1:20}'.format(count, token))
