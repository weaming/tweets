# coding: utf-8
# tweepy Status object
import re


def parse(tweets):
    if type(tweets) == list:
        return map(parse_tweet, tweets)
    else:
        return parse_tweet(tweets)


def parse_tweet(tweet_obj):
    entity_processors = {
        'hashtags': process_hash_tags,
        'symbols': process_symbols,
        'user_mentions': process_user_mentions,
        'urls': process_urls,
        'media': process_media
    }

    entities = tweet_obj.entities
    tweet_obj.html = tweet_obj.text

    # Process entities
    for entity, value in entities.items():
        if entity not in entity_processors:
            pass

        # get more photos
        if entity == 'media':
            value = tweet_obj.extended_entities['media']

        entity_processors[entity](value, tweet_obj)

    return tweet_obj.html


def process_hash_tags(tags, tweet):
    for tag in tags:
        text = tag['text']
        anchor = u'<a class="tag" href="https://twitter.com/hashtag/{0}">#{0}</a>'.format(
            text)
        tweet.html = tweet.html.replace('#' + text, anchor)


def process_symbols(symbols, tweet):
    pass


def process_user_mentions(users, tweet):
    for user in users:
        tweet.html = tweet.html.replace(
            '@%s' % user['screen_name'],
            u'<a class="at" href="https://twitter.com/{0}">@{1}</a>'.format(
                user['screen_name'], user['name']))


def process_urls(urls, tweet):
    for url in urls:
        tweet.html = tweet.html.replace(
            url['url'], u'<a class="url" href="%s">%s</a>' %
            (url['expanded_url'], url['display_url']))


def process_media(medias, tweet):
    for media in medias:
        if media['type'] == 'video':
            source = ''
            for info in media['video_info']['variants']:
                source += '<source src="%s" type="%s">' % (
                    info['url'], info['content_type'])
            video = '<br/><video controls poster="%s">%s</video>' % (
                media['media_url'], source)
            tweet.html = tweet.html.replace(media['url'], video)

    photo_medias = list(filter(lambda x: x['type'] == 'photo', medias))
    if photo_medias:
        image_html_list = []
        for media in photo_medias:
            image = '<img src="%s"/>' % media['media_url']
            image_html_list.append(image)

        tweet.html = tweet.html.replace(media['url'],
                                        '<br/>' + ' '.join(image_html_list))
