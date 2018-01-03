import sys
import json
import time
import string

from tweepy import API
from tweepy import OAuthHandler

from tweepy import Cursor

from tweepy import Stream
from tweepy.streaming import StreamListener


# One option is to place your comsumer key, secrets, access token and secret in a local file 
# that we will call `config.py`.
from config import *

# contents of config.py file: 
# consumer_key    = 'XXXXXXXXXXXXXXXXXXXXX'
# consumer_secret = 'XXXXXXXXXXXXXXXXXXXXX' 
# access_token    = 'XXXXXXXXXXXXXXXXXXXXX'
# access_secret   = 'XXXXXXXXXXXXXXXXXXXXX'


# Authentication
def get_twitter_auth():
    """Setup Twitter Authentication.
    
    Return: tweepy.OAuthHandler object
    """
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth
    
def get_twitter_client():
    """Setup Twitter API Client.
    
    Return: tweepy.API object
    """
    auth = get_twitter_auth()
    client = API(auth)
    return client

client = get_twitter_client()


# Going through client's timeline
time.sleep(10)  # sleep for 10 secs, collect tweets and print them out.

for i, status in enumerate(Cursor(client.home_timeline).items(5)):
    print('{0}.)   {1}\n'.format(i+1, status.text))


# Getting client's tweets
"""If you get: TweepError: Twitter error response: status code = 429
Then you have exceeded your
"""
with open('home_timeline.jsonl', 'w') as f:
    for page in Cursor(client.home_timeline, count=200).pages(4):  # limit of 800 for you
        for status in page:
            f.write(json.dumps(status._json) + '\n')

            # with open('home_timeline.txt','w') as f:
            #    for page in Cursor(client.home_timeline, count=200).pages(4): # limit of 3200 for other user
            #        for status in page:
            #            f.write(json.dumps(status.text) +'\n')


# Getting @user's tweets
user = 'realDonaldTrump'
fname = 'usr_timeline_{}.jsonl'.format(user)
with open(fname, 'w') as f:
    for page in Cursor(client.user_timeline, screen_name=user, count=300).pages(16): # limit of 3200 for other user
        for status in page:
            f.write(json.dumps(status._json)+'\n')





# Visualization
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

fname = 'usr_timeline_realDonaldTrump.jsonl'
with open(fname, 'r') as f:
    all_dates = []
    for line in f:
        tweet = json.loads(line)
        all_dates.append(tweet.get('created_at'))

    idx = pd.DatetimeIndex(all_dates)
    ones = np.ones(len(all_dates))
    my_series = pd.Series(ones, index=idx)
    per_minute = my_series.resample('1Min').sum().fillna(0)



fig, ax = plt.subplots()

ax.plot(per_minute.index, per_minute)

plt.grid(True)
plt.title('Tweets Frequencies')
plt.ylatr

hours = mdates.MinuteLocator(interval=2)
date_formatter = mdates.DateFormatter('%H:%M')

#ax.xaxis.set_major_locator(hours)
#ax.xaxis.set_major_formatter(date_formatter)
#max_freq = per_minute.max()
#ax.set_ylim(0, max_freq)


