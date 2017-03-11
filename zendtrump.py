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

INTERVAL_MINS = os.environ['interval_mins']

def zendtrump():
    '''Usage: zendtrump
        This script reads a users' last tweet, and plants it on top of a relaxing image.

        Donald Trump needs to chill the fuck out.
    '''
    # get latest status
    target = "@RealDonaldTrump"
    twitter_api = twitter.Api(consumer_key=os.environ['consumer_key'],
                              consumer_secret=os.environ['consumer_secret'],
                              access_token_key=os.environ['access_token_key'],
                              access_token_secret=os.environ['access_token_secret'])

    user = twitter_api.GetUser(screen_name=target)
    last_status = user.status

    post_time_ascii = last_status.created_at
    post_time = datetime.datetime.strptime(post_time_ascii, '%a %b %d %H:%M:%S +0000 %Y')
    now = datetime.datetime.now()

    timediff = now - post_time
    if timediff > (INTERVAL_MINS * 60):
        return

    last_status_text = last_status.text

    #get search term
    with open('searchterms') as terms_file:
        lines = terms_file.readlines()
        terms = [x.strip() for x in lines]
        search_term = random.choice(terms)

    #get an image url
    flickr = FlickrAPI(os.environ['flickr_key'], os.environ['flickr_secret'], format='parsed-json')
    params = 'url_c'
    fifty_results = flickr.photos.search(text=search_term, per_page=50, extras=params)
    images = fifty_results['photos']['photo']
    result = random.choice(images)
    image_url = result['url_c']

    #do the needful
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
    last_status_text_no_ascii = ''.join([i if ord(i) < 128 else '' for i in last_status_text])

    last_status_text_no_ascii_no_urls = re.sub(r'http\S+', '', last_status_text_no_ascii, flags=re.MULTILINE)

    last_status_text_no_ascii_no_urls_no_newlines = string.join(last_status_text_no_ascii_no_urls.splitlines())

    image_link = pattern.sub(lambda x: replacements[x.group()], last_status_text_no_ascii_no_urls_no_newlines) + ".jpg"

    meme_image_link = "https://memegen.link/custom/" + image_link + "?alt=" + image_url

    temp_filename = next(tempfile._get_candidate_names())
    temp_fullpath = os.path.join(os.getcwd(), temp_filename)

    r = requests.get(meme_image_link, stream=True)

    if r.status_code == 200:
        with open(temp_fullpath, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    temp_file = open(temp_fullpath, 'rb')
    twitter_media_id = twitter_api.UploadMediaSimple(temp_file)
    twitter_api.PostUpdate(status="", media=twitter_media_id)

    print "done"

def main():

    zendtrump()

    sched = BlockingScheduler()
    sched.add_job(zendtrump, 'interval', minutes=INTERVAL_MINS)

    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    main()
