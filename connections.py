# -*- coding: utf-8 -*-
"""
Created on 02/09/2021
@author: Kelvin
@github: gitpinto
"""

#Importing required libraries
from pymongo import MongoClient
from static import constants
import tweepy
import pytumblr


#MongoDB Connections
client = MongoClient(constants.mongo.CONN_STRING)
db = client.get_database(constants.mongo.DB_NAME)
twitterCol = db[constants.mongo.TWITTER_COL]
tumblrCol = db[constants.mongo.TUMBLR_COL]

#Twitter API Connections
twitterAuth = tweepy.OAuthHandler(constants.twitter.CONSUMER_KEY, constants.twitter.CONSUMER_SECRET)
twitterAuth.set_access_token(constants.twitter.ACCESS_TOKEN, constants.twitter.ACCESS_TOKEN_SECRET)
twitterAPI = tweepy.API(twitterAuth,wait_on_rate_limit=True)

#Tumblr API Connections
tumblrClient = pytumblr.TumblrRestClient(
    constants.tumblr.CONSUMER_KEY,
    constants.tumblr.CONSUMER_SECRET,
    constants.tumblr.OAUTH_TOKEN,
    constants.tumblr.OAUTH_TOKEN_SECRET
)