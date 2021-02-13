# -*- coding: utf-8 -*-
"""
Created on 02/09/2021
@author: Kelvin
@github: gitpinto
"""
class mongo:
    'MongoDB Credentials'
    CONN_STRING = 'Your MongoDB Connection String'
    DB_NAME = 'Your MongoDB Database'
    TWITTER_COL= 'Your MongoDB Collection to store twitter Data'
    REDDIT_COL= 'Your MongoDB Collection to store Reddit Data'

class twitter:
    'Twitter Credentials'
    CONSUMER_KEY= 'Your Twitter Consumer Key'
    CONSUMER_SECRET= 'Your Twitter Consumer Secret'
    ACCESS_TOKEN= 'Your Twitter Access Token'
    ACCESS_TOKEN_SECRET= 'Your Twitter Access Token Secret'
    USERNAME = 'Your Twitter username'


class tumblr:
    'Tumblr Credentials'
    CONSUMER_KEY= 'Your Tumblr Consumer Key'
    CONSUMER_SECRET= 'Your Tumblr Consumer Secret'
    OAUTH_TOKEN= 'Your Tumblr OAUTH Token'
    OAUTH_TOKEN_SECRET='Your Tumblr OAUTH Token Secret'
    BLOG_NAME = 'Your Tumblr blogname'

class files:
    'Class of constants to store uploaded files'
    fileStorePath = 'static/storage/'
