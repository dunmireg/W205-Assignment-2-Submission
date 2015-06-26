import os.path
import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
import codecs
import pylab as pl
import numpy as np
import re

#Check if a result file already exists
if not os.path.exists("result.txt"):
    hashtag = "<>" #hashtag marker
    num_files = "<>" #how many files exist
    list_of_files = []

#collect a list of all the text files with the hashtag supplied
    for i in range(0, num_files):
        fname = fname = hashtag+"-tweetsText-"+str(i+1) +".txt"
        list_of_files.append(fname)

#create a result file to store all the text. This loops through all the text files,
#lowercases all the words, and adds them to the result file
    with open("result.txt", "wb") as outfile:
        for f in list_of_files:
            with open(f, "rb") as infile:
                for line in infile:
                    line = line.lower()
                    outfile.write(line)

#Read the result file using utf-8, use nltk to tokenize the results, then get a frequency distribution
file = codecs.open("result.txt", "r", "utf-8")
text = file.read()
tokens = nltk.word_tokenize(text) #tokenize text
fdist = FreqDist(tokens) #create a frequency distribution
common = fdist.most_common(1000) #get the 1,000 most common words
stopwords = nltk.corpus.stopwords.words('english') #add stopwords
fdist2 = {} #empty dictionary to store results
i = 0

#while there are less than 30 words in the dictionary, loop over the resutls
while len(fdist2) <= 30:
    curr = common[i]
    if curr[0] not in stopwords and re.match('^[a-zA-Z0-9]*$',curr[0]): #use regular expression to check if a word and not a special character
        fdist2[curr[0].encode('ascii')] = curr[1] #encode as ascii and add to dictionary
    i += 1

print fdist
print fdist2

#create a plot of the frequency distribution
X = np.arange(len(fdist2))
pl.bar(X, fdist2.values(), align = 'center', width = 0.5)
pl.xticks(X, fdist2.keys())
locs, labels = pl.xticks()
pl.setp(labels, rotation = 90)
ymax = max(fdist2.values()) + 100
pl.ylim(0, ymax)
pl.suptitle("<>")
pl.show()
