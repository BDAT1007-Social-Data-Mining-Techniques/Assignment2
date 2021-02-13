# -*- coding: utf-8 -*-
"""
Created on 02/09/2021
@author: Kelvin
@github: gitpinto
"""

#Importing required libraries

import connections as conn
from flask import Flask, render_template, json, jsonify, Response, request, redirect
from static import constants
import string
import random

app = Flask(__name__)

def get_Twitter_Data():
    'Function to get the data from Twitter and store in Mongo DD'
    conn.twitterCol.drop() #Drop the existing collection in MongoDB
    i = 1
    for status in conn.twitterAPI.user_timeline(constants.twitter.USERNAME):
        tweetData = {
            "status_num": i,
            "status_text": status.text,
            "status_name": status.user.name,
            "status_createdAt": status.created_at,
            "status_favouriteCount": status.favorite_count,
            "status_lang": status.lang
        } #Data Model for twitter data
        conn.twitterCol.insert_one(tweetData) #Insert data to MongoDB
        i+=1

def get_Tumblr_Data():
    conn.tumblrCol.drop() #Drop the existing collection in MongoDB
    data = conn.tumblrClient.posts(constants.tumblr.BLOG_NAME) #Get data of posts on a blog
    postData = []
    p = data['posts']
    i = 1
    for element in p:
        trailData = element['trail']
        blogContent = ""
        for blog in trailData:
            blogContent = blog['content']
        data = {
            "post_number": i,
            "post_type": element['type'],
            "post_url": element['post_url'],
            "post_createdAt": element['date'],
            "post_title": element['summary'],
            "post_content": blogContent,
        } #Data Model for tumblr data
        postData.append(data)
        i+=1
    conn.tumblrCol.insert_many(postData) #Insert Data to MongoDB

#Default Route for index page
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

#Default route for get_Twitter_Data() method
@app.route('/api/getTwitter')
def get_tweets():
    get_Twitter_Data()
    return redirect('/') 

#Default route for get_Tumblr_Data() method
@app.route('/api/getTumblr')
def get_tumblr():
    get_Tumblr_Data()
    return redirect('/') 

#endpoint for the API tp get tweet data from MongoDB and disaply on website
@app.route('/api/viewTweets')
def view_tweets():
    # empty array to store data
    output = []
    #get data from MongoDB and store it in the array
    for s in conn.twitterCol.find():
        del s['_id']
        output.append(s)
    #create json object to pass to template
    data = {
        "data": output
    }
    return jsonify(data)

#endpoint for the API to get Tumblr posts from MongoDB and display on the site
@app.route('/api/viewTumblr')
def view_tumblr():
    # empty array to store data
    output = []
    #get data from MongoDB and store it in the array
    for s in conn.tumblrCol.find():
        del s['_id']
        output.append(s)
    #create json object to pass to template
    data = {
        "data": output
    }
    return jsonify(data)

#endpoint for the POST API that posts a tweet on Twitter
@app.route('/api/postTwitter', methods = ['POST', 'GET'])
def post_tweet():
    if request.method == 'POST':
        tweetText= str(request.form['tweetText']) #Get the Tweet Text from the frontend form
        conn.twitterAPI.update_status(tweetText) #Post tweet to Twitter using Tweepy
    get_Twitter_Data()  #calling get_Twitter_Data() method to store the data from Twitter to MongoDB
    return redirect('/') 

#endpoint for the POST API that posts on Tumblr
@app.route('/api/postTumblr', methods = ['POST', 'GET'])
def post_tumblr():
    if request.method == 'POST':
        tumblrTitle= str(request.form['tumblrTitle']) #Get the Post Title from the frontend form
        tumblrText= str(request.form['tumblrText']) #Get the Post Text from the frontend form
        imFile = request.files['imFile'] #Get the uploaded image from the frontend form
        if imFile.filename != '':
            caption = "Title: " + tumblrTitle + '\n\nBody: ' + tumblrText 
            res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7)) #generating a random string to store the file in local storage
            filePath = constants.files.fileStorePath + str(res) + '-' + imFile.filename #Generate a filepath to store the file
            imFile.save(filePath) #Save the uploaded file in FilepAth
            conn.tumblrClient.create_photo(constants.tumblr.BLOG_NAME, state="published",
                    caption=caption,
                    data=filePath) #Post the photo to Tumblr
        else:
            #Post the text to Tumblr
            conn.tumblrClient.create_text(constants.tumblr.BLOG_NAME, state="published", title=tumblrTitle, body=tumblrText)
    get_Tumblr_Data() #Call method get_Tumblr_Data() to get the data from Tumblr and store in MongoDB
    return redirect('/') 
    


if __name__ == '__main__':
    app.run()