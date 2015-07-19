# W205-Assignment-2-Submission - Ted Dunmire

This is the README for Assignment 2 for Summer 2015 W205.

##Part 1: Twitter Acquisition

This refers to the getTweets.py script. This code will retrieve a weeks worth of tweets using the Twitter
search api and store the results as a series of json and text files. For this I initialize a TweetSerializer
based off the one from class, which opens a new file text file and json file, writes the tweets to the appropriate
file and then closes the file. Each hashtag has its own TweetSerializer to handle this writing. The separate hashtags
are used in the naming of the files to make it easy to distinguish them.

Then the grabTweets function actually gets the tweets, using the Twitter search api. The parameters are specified
above (the dates used) and I chose to restrict the tweets to only English tweets. For resiliency I put the chunk of
code into a while loop, taking advantage of the Cursor object being iterable. As long as there are more tweets that the
Cursor has retrieved, the loop will execute (it breaks on a StopIteration exception when there are no more tweets). This has the
advantage of continually executing. Occasionally a TweepError will get thrown, usually when the connection has timed out. For this
I catch the exception and pause the while loop for 15 minutes, then reinitialize the search api using the tweet.id of the last tweet
I retrieved. This means that the error just causes pausing and then the program picks up where I left off.

For chunking I decided to write out files of 1,000 tweets. This is handled in the grabTweets function, which keeps a counter of how
many tweets have been written and determines if it will start a new file (using the TweetSerializer) or end the existing file through
the modulo operator.

In total the execution took approximately 10 hours and retrieved approximately 190,000 tweets that are relevant.

##Part 2: s3

I decided to manually upload my files into AWS. They can be found here in the bucket tdw205archive:
https://tdw205archive.s3.amazonaws.com/

Each hashtag has its own folder under the relevant header and furthermore within each folder is a separate
folder for the text files and the json files.

##Part 3: Histograms

This refers to the distribution.py file. In this the first thing the script does is check
for the existence of a "result.txt" file. If this does not exist what the script does is get a list of
all the file names (text specifically, ignoring json) for the relevant hashtag. Then it creates a new
file and adds the lines of each of the existing text files to the result file one by one (lowercasing the letters
of these files as it goes). At the end I have one big file called result that is an aggregation of all the text
from the tweets.

Then, using nltk I read the result file in and tokenize the words. Then I use nltk's FreqDist() function to
get a frequency distribution of the words, describing how many times they occur. Then I create an empty dictionary
and start a while loop (I restricted the most_common call to the first 1,000 most common words but this is arbitrary).
While there are less than 30 words in the dictionary, the loop goes through each of the words in returned by most_common,
from most common to least common. It checks that a word does not exist in the english stopwords list (provided by nltk)
and checks that the word matches a regular expression of just letters and numbers (thus avoiding special characters like '#').

Finally this list of the 30 most common words is used as the basis to create a histogram showing frequency and saved as a png file.
These histograms can be found in the Histograms folder. 
