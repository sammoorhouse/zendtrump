import re
import string

def split_tweet(tweet_text):
    '''splits a tweet into two sections'''

    print tweet_text
    words = tweet_text.split(' ')
    last_word = words[-1]

    sentences = tweet_text.split('.')

    if len(sentences) is 2 and abs(len(sentences[0]) - len(sentences[1])) < 5:
        # two similar-length sentences?
        print "1"
        top = sentences[0]
        bottom = sentences[1]
    elif len(sentences) > 1 and sentences[-1].endswith('!'):
        print "2"
        # big ending. Excellent!
        top = '.'.join(sentences[:-1]) + "."
        bottom = sentences[-1]
    elif len(sentences) > 1 and len(sentences[-1].split(' ')) < 5:
        print "3"
        #less than 5 words in the final sentence?
        top = '.'.join(sentences[:-1]) + "."
        bottom = sentences[-1]
    elif last_word in ["#MAGA", 'Sad!', 'sad!', 'Weak!']:
        print "4"
        # famous last words?
        top = ' '.join(words[:-1])
        bottom = words[-1] #this is somehow a string
    else:
        print "5"
        #split into two
        half = int(len(words)/2)
        top = ' '.join(words[0:half])
        bottom = ' '.join(words[half:])

    return (top.strip(), bottom.strip())

def memegen_replace(tweet):
    '''replaces some uri-like characters for memegen'''
    tweet = re.sub(r"\s+", "-", tweet)
    tweet = re.sub("_", "__", tweet)
    tweet = re.sub(r"\?", "~q", tweet)
    tweet = re.sub("%", "~p", tweet)
    tweet = re.sub("#", "~h", tweet)
    tweet = re.sub("/", "~s", tweet)
    tweet = re.sub("\\\"", "\'\'", tweet)

    return tweet

def clean_tweet_text(tweet):
    '''removes unicode strings and URLs'''

    # mostly robbed from https://github.com/lukewrites/sealdonaldtrump/blob/master/tweet_getter.py
    tweet = ''.join([i if ord(i) < 128 else '' for i in tweet]) #high ascii
    tweet = re.sub(r"https?\:\/\/", "", tweet)   #links
    tweet = re.sub(r"t.co\/([a-zA-Z0-9]+)", "", tweet)
    tweet = re.sub(r"bit.ly\/([a-zA-Z1-9]+)", "", tweet)
    tweet = re.sub(r"Video\:", "", tweet)        #Videos
    tweet = re.sub(r"\n", "-", tweet)             #new lines
    tweet = re.sub(r"&amp;", "and", tweet)       #encoded ampersands

    # split tweet here
    (top, bottom) = split_tweet(tweet)
    top = memegen_replace(top)
    bottom = memegen_replace(bottom)

    image_link = top + "/" + bottom + ".jpg"
    return image_link

def main():
    '''main'''
    res = clean_tweet_text("Thank you Nashville, Tennessee!")
    print res

if __name__ == "__main__":
    main()
