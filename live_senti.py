import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import re

# import nltk
# nltk.download('punkt')

# These keys and token can be obtained easily using twitter developer account
ckey = 'your ckey'
csecret = 'your csecret key'
atoken = 'your account token'
asecret = 'your secret token'

"""Tag for analysis"""
tag = 'place your tag here'

def calctime(a):
    return time.time()-a


positive, negative, compound = 0, 0, 0
count = 0
axislimit = 20
timelimit = 40
initime = time.time()
plt.ion()


class listener(StreamListener):

    def on_data(self, data):
        global initime
        t = int(calctime(initime))
        all_data = json.loads(data)
        tweet = all_data["text"]
        # username=all_data["user"]["screen_name"]
        # print(type(tweet))
        tweet = " ".join(re.findall("[a-zA-Z]+", tweet))
        blob = TextBlob(tweet.strip())

        global positive
        global negative
        global compound
        global count
        global axislimit
        global timelimit

        count = count + 1
        senti = 0
        for sen in blob.sentences:
            senti = senti + sen.sentiment.polarity
            if sen.sentiment.polarity >= 0:
                positive = positive + sen.sentiment.polarity
            else:
                negative = negative + sen.sentiment.polarity
        compound = compound + senti
        print('Count: ', count)
        print('Tweet: ', tweet.strip())
        print('Sentiments: ', senti)
        print('Time: ', t)
        print(str(positive) + ' ' + str(negative) + ' ' + str(compound))

        if timelimit-t < 3:
            timelimit += 20
        if axislimit-positive < 3 or axislimit-abs(negative) < 3:
            axislimit += 10
        plt.axis([0, timelimit, -axislimit, axislimit])
        plt.title('Live Sentiment analysis of ' + tag)
        plt.xlabel('Time')
        plt.ylabel('Sentiment')
        plt.plot([t], [positive], 'go', [t], [negative], 'ro', [t], [compound], 'bo')
        plt.axhline(0, color='black')
        plt.show()  
        plt.pause(0.0001)

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=[tag])

