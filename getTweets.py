import sys
import tweepy
import datetime
import signal
import json
import csv
import time
from boto.s3.connection import S3Connection
from boto.s3.key import Key

#Chunking module
#This program opens a new file, writes tweets to the file, and handles closing the file
#Each hashtag will have a serializer that will handle the files and writing them out.
#The file will have 1,000 tweets
class TweetSerializer:
   out = None #json file pointer
   out2 = None #text file pointer
   first = True
   count = 0

   def __init__(self, hashtag):
       self.hashtag = hashtag

   def start(self):
      self.count += 1
      fname = str(self.hashtag)+"-tweets-"+str(self.count)+".json"
      fname2 = str(self.hashtag)+"-tweetsText-"+str(self.count)+".txt"
      self.out = open(fname,"w")
      self.out2 = open(fname2, "w")
      self.out.write("[\n")
      self.out2.write("[\n")
      self.first = True

   def end(self):
      if self.out is not None:
         self.out.write("\n]\n")
         self.out.close()
         self.out2.write("\n]\n")
         self.out2.close()
      self.out = None
      self.out2 = None

   def write(self,tweet):
      if not self.first:
         self.out.write(",\n")
         self.out2.write(",\n")
      self.first = False
      self.out.write(json.dumps(tweet._json).encode('utf8')) #add json
      self.out2.write(tweet.text.encode('utf8')) #add text


consumer_key = "<>"
consumer_secret = "<>"

access_token = "<>"
access_token_secret = "<>"

#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret) #Using AppAuth
api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True) #use twitter API
sinceDate = "2015-06-14"
untilDate = "2015-06-22"

#handles actually retrieving tweets from the search api for a week
def grabTweets(query, serializer):
    ts_1_count = 0 #count of how many tweets collected, used for chunking (create files of 1000 tweets)
    ts_1_id = None #variable to store the id of a tweet for resiliency
    searchCursor = tweepy.Cursor(api.search,q=query, since = sinceDate, until = untilDate, max_id = ts_1_id, lang = "en").items()
    while True:
        try:
            tweet = searchCursor.next()
            ts_1_id = tweet.id
            if ts_1_count%1000 == 0:
                serializer.start()
            serializer.write(tweet)
            if ts_1_count%1000 == 999:
                serializer.end()
            ts_1_count += 1
        except tweepy.TweepError as e: #handle resiliency by encountering error and backing off for 15 minutes and restarting from tweet id
            print "TweepError found sleeping for 900 seconds"
            time.sleep(900)
            searchCursor = tweepy.Cursor(api.search, q1, since_id = ts_1_id, lang = "en").items()
            continue
        except StopIteration:
            break


q1 = "%23NBAFinals2015 -%23Warriors"
q2 = "%23Warriors -%23NBAFinals2015"
q3 = "%23NBAFinals2015 %23Warriors"

ts1 = TweetSerializer("#NBAFinals2015")
ts2 = TweetSerializer("#Warriors")
ts3 = TweetSerializer("#NBAFinals2015 #Warriors")


grabTweets(query = q1, serializer = ts1)
grabTweets(query = q2, serializer = ts2)
grabTweets(query = q3, serializer = ts3)
