#!/usr/bin/env python
# coding: utf-8
import json, re

import tweepy
from flask import Flask, jsonify, request, Response
from tweet2html import parse
from config import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

API = tweepy.API(auth)
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def hello_world():
    return 'Converting tweets to HTML in JSON format. Star/Fork me: https://github.com/weaming/tweets'


def tweet_to_html(tweet):
    txt0 = re.sub(r'(http[\w:/.?&#]{5,})', r'<a class="link" href="\1">\1</a>',
                  tweet.text)
    txt1 = re.sub(r'@(\w+)',
                  r'<a class="at" href="https://twitter.com/\1">@\1</a>', txt0)
    return txt1


def get_user_info(user):
    keys = [
        'created_at',
        'description',
        'followers_count',
        'following',
        'friends_count',
        'lang',
        'location',
        'muting',
        'name',
        'profile_background_image_url',
        'profile_background_image_url_https',
        'profile_image_url',
        'profile_image_url_https',
        'protected',
        'screen_name',
        'statuses_count',
    ]
    return {
        k: getattr(user, k) if k != 'created_at' else str(getattr(user, k))
        for k in keys
    }


@app.route('/followers')
def followers():
    user_id = request.args.get('id', app_conf['twitter_id'])
    my_tweets = API.followers(
        id=user_id,
        cursor=-1,
    )
    users = my_tweets[0]
    users_data = list(map(get_user_info, users))
    rv = json.dumps({
        'followers': users_data,
        'count': len(users_data),
        'user_id': user_id,
    })

    resp = Response(rv)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp


def get_return_value(tweets, request):
    if request.args.get('raw'):
        rv_data = [x._json for x in tweets]
    else:
        rv_data = [parse(x) for x in tweets]
    return rv_data


@app.route('/tweets')
def tweets():
    my_tweets = API.user_timeline(
        id=request.args.get('id', app_conf['twitter_id']),
        count=request.args.get('count', 20),
        page=request.args.get('page', 0))

    rv_data = get_return_value(my_tweets, request)
    rv = json.dumps(rv_data, ensure_ascii=False)

    resp = Response(rv)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/favorites')
def favorites():
    my_tweets = API.favorites(
        id=request.args.get('id', app_conf['twitter_id']),
        count=request.args.get('count', 20),
        page=request.args.get('page', 0))

    rv_data = get_return_value(my_tweets, request)
    rv = json.dumps(rv_data, ensure_ascii=False)

    resp = Response(rv)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp
