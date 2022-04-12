# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 14:50:47 2022

@author: Tommy Huynh
"""

api_key = "uR37r67AcjKfHQD2FqLTJvTzK"
api_secret = "980Vgt9sV66a5QMrM4LZXw6S0DaCckGEsv60nti8f269oDzP31"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAKXPawEAAAAA%2B48beXcy8VBo6xqsZKVWRx8THAs%3De9XKEuKj9Amh6UdxtRL2tOq7aj8r6Majsut3IbzkhrB5fbbga6"

import requests
import os
import json
import pandas as pd


def create_url():
    base = "https://api.twitter.com/2/tweets/sample/stream"
    fields = "tweet.fields=created_at,entities,source,possibly_sensitive,lang"
    expansions = "expansions=author_id,geo.place_id"
    userfields = "user.fields=created_at,location,username"
    return base +"?" + "&".join([fields,expansions,userfields])

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2SampledStreamPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth, stream=True)
    print(response.status_code)
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            yield json.dumps(json_response, indent=4, sort_keys=True)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )

def fetchsamples():
    return connect_to_endpoint(create_url())


# test the function: retrieve 10 tweets
streamer = fetchsamples()
for _ in range(10):
   print(next(streamer))

streamer = fetchsamples()
# now collect 1,000 tweets
tweets = [next(streamer) for _ in range(1000)]

# The expression above is called a list comprehension -- they are very useful!   
# It creates a list by iterating over another list.
# https://www.w3schools.com/python/python_lists_comprehension.asp

#Extracting Tweet
#parses each line and filter our non-english tweets
import json

tweets_eng = []

for tweet in tweets: 
    tweet_object = json.loads(tweet)
    
    if tweet_object['data']['lang'] == 'en':
        text = tweet_object['data']['text']
        tweets_eng.append(text)
    else:
        pass
    
#Estimating Sentiment     
# for each tweet:
#  initialize tweet score
#  for each word in the tweet:
#      look up score for that word in AFINN-111.txt
#      if found, add the score to the running total
#  print score for each tweet

scores = {}

sentiment = open("AFINN-111.txt", "r")

for line in sentiment: 
    word, score = line.split("\t")
    scores[word] = int(score)
    
print(scores)

listScores = []

for tweet in tweets_eng:
    tweetWords = []
    listWords = tweet.split()
    score = 0
    for word in listWords:
        if word in scores:
            score += scores[word]
    listScores.append(score)
    
print(listScores)

#Building an Inverted Index
wordsList = list(scores.keys())

#Intialized inverted index 
inverted_index = {}

for tweet in tweets_eng:
    for word in wordsList:
        if word in tweet:
           #if there isn't already a value assigned to the key, a new list will be created 
           if not word in inverted_index:
                inverted_index[word] = []
           #Append the new list to existing list 
           inverted_index[word].append(str(tweet))
           
print(inverted_index)

#Compute Term Frequency
# for each w in any tweet, return the number of tweets it appears in
#calculate size of list and add 

for key, value in inverted_index.items():
    print(key, len(list(filter(bool, value))))
    
#Derive the sentiment of unseen terms
# one approach:
# Step 1: Compute sentiment for every tweet (you already did this)
# Step 2: Associate every term with a list of tweet se that contain it (you already did this)
# Step 3: For each term, compute the average sentiment of all tweets that contain it

#Initialize new index with words from wordsList
new_index = {i : 0.0 for i in wordsList}

#Loops through each term in wordsList 
for word in wordsList:
    #tracks sentiment score of tweet
    sentiment_score = 0
    for i in range(len(tweets_eng)):
        count = 1
        if word in tweets_eng[i]:
            #adds sentiment score and updates count 
            sentiment_score += listScores[i]
            count += 1
        #calculates average of each word 
        new_index[word] = (sentiment_score / count)

#prints out new dictionary 
for word in wordsList:
    print(word, new_index[word])


#Sentiment by State        
# create a dictionary to hold State -> (sum_of_sentiment, count)
# for each tweet t
#   determine the state s associated with t.  If you can't, it's ok to go on to the next tweet
#   add sentiment(t) to the total for s, and also increment the count so you can compute the average.
# for each state, divide sum of sentiment by the count to compute the average
# sort this list by average score.

#I couldn't figure out how to pull location data from the tweets
#This set of tweets include location data 
#tweets_eng = []

#for tweet in tweets: 
#    tweet_object = json.loads(tweet)
    
#    if tweet_object['data']['lang'] == 'en':
#            if tweet_object['includes']['users'][0]['location']: 
 #               data = tweet_object['data']['text'], tweet_object['includes']['users'][1]['location']
 #               tweets_eng.append(text)
 #   else:
 #s       pass

#initalize new dictionary with states
states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

statesList = {i : (0.0, 0)  for i in states}

#for tweet in tweets:
#    tweet_object = json.loads(tweet)
#    sentiment_score = 0 
#    for key in states.keys():
#        count = 1
#        if str(states.keys()) in tweet_object['includes']['users'][1]['location']:
#            sentiment_score += listScores[i]
#            count += 1
#            statesList[states[key]] = (sentiment_score / count)
                
#print(statesList)


#Top 10 hashtags with highest sentiment scores 
# create a dictionary to hold hashtag -> (sum_of_sentiment, count)
# for each tweet t
#   extract the list of hashtags associated with the tweet.
#   for each hashtag h
#      put it in the dictionary if it's not there already
#      add sentiment(t) to the total for h, and also increment the count so you can compute the average.
# for each hashtag, divide sum of sentiment by the count to compute the average
# sort this list by average score.

#I could not figure out how to pull hashtag data from the tweets 

hashtag_dict = {}

for tweet in tweets:
    tweet_object = json.loads(tweet)
    sentiment_score = 0 
    for hashtag in hashtag_dict.keys():
        count = 1
        if str(hashtag_dict()) in tweet_object['data']['entities']['hashtags']:
            sentiment_score += listScores[i]
            count += 1
            statesList[states[key]] = (sentiment_score / count)








