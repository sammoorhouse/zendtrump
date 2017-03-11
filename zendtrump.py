#!/usr/bin/env python

'''Post a relaxing message to twitter'''

import os
import random
import re
import shutil
import ssl
import string
import tempfile
import datetime

import requests
import twitter
from apscheduler.schedulers.blocking import BlockingScheduler
from flickrapi import FlickrAPI

INTERVAL_MINS = int(os.environ['interval_mins'])
LAST_TWEET_OVERRIDE = bool(os.environ['last_tweet_override'])

def get_search_term(filename):
    '''returns a random line from the given file'''

    with open(filename) as terms_file:
        lines = terms_file.readlines()
        terms = [x.strip() for x in lines]
        search_term = random.choice(terms)
    return search_term

def get_last_tweet_for_user(twitter_api, user):
    '''returns a Status object representing the users last tweet'''

    user = twitter_api.GetUser(screen_name=user)
    return user.status


def get_image_url_for_searchterm(flickr_api, search_term):
    '''returns the url for an image fulfilling the search term'''

    params = 'url_c'
    fifty_results = flickr_api.photos.search(text=search_term, per_page=50, extras=params)
    images = fifty_results['photos']['photo']
    result = random.choice(images)
    while params not in result:
        result = random.choice(images)

    image_url = result[params]
    return image_url

def clean_tweet_text(last_status_text):
    '''removes unicode strings and URLs, and replaces some uri-like
    characters for memegen'''

    replacements = {
        ' ':'_',
        '_':'__',
        '\?':'~q',
        '%':'~p',
        '#':'~h',
        '/':'~s',
        '\\\"':'\'\''
    }

    pattern = re.compile('|'.join(replacements.keys()))
    no_ascii = ''.join([i if ord(i) < 128 else '' for i in last_status_text])
    no_ascii_no_urls = re.sub(r'http\S+',
                              '',
                              no_ascii,
                              flags=re.MULTILINE)
    no_ascii_no_urls_no_newlines = string.join(no_ascii_no_urls.splitlines())
    image_link = pattern.sub(lambda x: replacements[x.group()],
                             no_ascii_no_urls_no_newlines) + ".jpg"
    return image_link

def zendtrump():
    '''Usage: zendtrump
        This script reads a users' last tweet, and plants it on top of a relaxing image.

        Donald Trump needs to chill the fuck out.
    '''

    twitter_api = twitter.Api(consumer_key=os.environ['consumer_key'],
                              consumer_secret=os.environ['consumer_secret'],
                              access_token_key=os.environ['access_token_key'],
                              access_token_secret=os.environ['access_token_secret'])

    flickr_api = FlickrAPI(os.environ['flickr_key'],
                           os.environ['flickr_secret'],
                           format='parsed-json')

    # get latest status
    target = "@RealDonaldTrump"

    last_status = get_last_tweet_for_user(twitter_api, target)
    post_time_ascii = last_status.created_at
    post_time = datetime.datetime.strptime(post_time_ascii, '%a %b %d %H:%M:%S +0000 %Y')
    now = datetime.datetime.now()

    timediff = now - post_time
    print "latest tweet was " + str(timediff.seconds) + " seconds ago"

    if timediff.seconds > (INTERVAL_MINS * 60) and not LAST_TWEET_OVERRIDE:
        print "skipping this run"
        return

    last_status_text = last_status.text

    #get search term
    search_term = get_search_term('searchterms')
    print "chosen search term \"" + search_term + "\""

    #get an image url
    image_url = get_image_url_for_searchterm(flickr_api, search_term)
    print "found image: " + image_url

    #clean up the text
    clean_status_text = clean_tweet_text(last_status_text)
    print "cleaned up status text: \"" + clean_status_text + "\""

    meme_image_link = "https://memegen.link/custom/" + clean_status_text + "?alt=" + image_url
    print "meme image link: " + meme_image_link

    temp_filename = next(tempfile._get_candidate_names())
    temp_fullpath = os.path.join(os.getcwd(), temp_filename)

    request = requests.get(meme_image_link, stream=True)

    if request.status_code == 200:
        with open(temp_fullpath, 'wb') as downloaded_image_file:
            request.raw.decode_content = True
            shutil.copyfileobj(request.raw, downloaded_image_file)
    print "downloaded file: " + temp_fullpath

    temp_file = open(temp_fullpath, 'rb')
    twitter_media_id = twitter_api.UploadMediaSimple(temp_file)
    twitter_api.PostUpdate(status='#zenDonald', media=twitter_media_id)
    print "tweet posted"

    print "done"

def main():
    '''main'''

    print "initial execution"
    zendtrump()

    print "setting up timer"
    sched = BlockingScheduler()
    sched.add_job(zendtrump, 'interval', minutes=INTERVAL_MINS)

    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    main()
