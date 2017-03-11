#!/usr/bin/env python

'''Post a relaxing message to twitter'''

import os
import random
import re
import shutil
import ssl
import string
import tempfile

import requests
import twitter
from apscheduler.schedulers.blocking import BlockingScheduler
from flickrapi import FlickrAPI

INTERVAL_MINS = 30

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

    print "1: " + last_status_text

    last_status_text_no_ascii = ''.join([i if ord(i) < 128 else '' for i in last_status_text])

    print "2: " + last_status_text_no_ascii

    last_status_text_no_ascii_no_urls = re.sub(r'http\S+', '', last_status_text_no_ascii, flags=re.MULTILINE)

    print "3: " + last_status_text_no_ascii_no_urls

    last_status_text_no_ascii_no_urls_no_newlines = string.join(last_status_text_no_ascii_no_urls.splitlines())

    print "4: " + last_status_text_no_ascii_no_urls_no_newlines

    image_link = pattern.sub(lambda x: replacements[x.group()], last_status_text_no_ascii_no_urls_no_newlines) + ".jpg"

    print "5: " + image_link

    meme_image_link = "https://memegen.link/custom/" + image_link + "?alt=" + image_url

    print "AFTER: " + meme_image_link

    temp_filename = next(tempfile._get_candidate_names())
    temp_fullpath = os.path.join(os.getcwd(), temp_filename)

    print temp_filename

    r = requests.get(meme_image_link, stream=True)
    print "STATUS CODE = " + str(r.status_code)
    
    if r.status_code == 200:
        with open(temp_fullpath, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    print "file saved: " + temp_fullpath

    temp_file = open(temp_fullpath, 'rb')
    meme_image_data = temp_file.read()
    twitter_media_id = twitter_api.UploadMediaSimple(temp_file)
    twitter_api.PostUpdate(status="", media=twitter_media_id)

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
