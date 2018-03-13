#!/usr/bin/env python
# coding: utf-8

import base64
import json
import requests
from config import *


def get_token():
    bearer_token_credentials = '%s:%s' % (consumer_key, consumer_secret)
    encoded_credentials = base64.b64encode(bearer_token_credentials)

    url = 'https://api.twitter.com/oauth2/token'
    headers = {
        'Authorization': 'Basic %s' % encoded_credentials,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'User-Agent': 'http://bitsflow.org',
    }
    body = 'grant_type=client_credentials'

    res = requests.post(url, headers=headers, data=body)
    res_dict = json.loads(res.text)
    token_type, access_token = res_dict[u'token_type'], res_dict[u'access_token']
    assert token_type == 'bearer'
    return access_token


def get_timeline(count=10):
    timeline_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=%s&count=%s' % (app_conf['user_id'], count)

    timeline_response = requests.get(timeline_url, headers={'Authorization': 'Bearer %s' % access_token})
    timeline_dict = json.loads(timeline_response.text)
    return timeline_dict


if __name__ == '__main__':
    res = get_timeline(count=10)
    print json.dumps([x['text'].encode('utf-8') for x in res], ensure_ascii=False, indent=4)
