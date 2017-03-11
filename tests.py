'''tests for zendtrump'''

import unittest
import zendtrump

class TestStringMethods(unittest.TestCase):
    '''tests for tweet split methods'''

    def test_simple_split(self):
        '''with no special cases matching, should split
        the input roughly down the middle'''

        tweet = 'hello world'

        (top, bottom) = zendtrump.split_tweet(tweet)

        self.assertEquals(top, "")
        self.assertEquals(bottom, "hello world")

    def test_long_simple_split(self):
        '''simple split should work for long sentences too'''

        tweet = "LinkedIn Workforce Report: January and February were the strongest consecutive months for hiring since August and September 2015"

        (top, bottom) = zendtrump.split_tweet(tweet)

        self.assertEquals(top, "LinkedIn Workforce Report: January and February were the strongest")
        self.assertEquals(bottom, "consecutive months for hiring since August and September 2015")

    def test_last_word(self):
        '''if the last word is '#maga' or 'sad!' or similar,
        that should always be the second in the split'''

        tweet = "Weekly Address - 11:00 A.M. at the @WhiteHouse! #MAGA"

        (top, bottom) = zendtrump.split_tweet(tweet)

        self.assertEquals(top, "Weekly Address - 11:00 A.M. at the @WhiteHouse!")
        self.assertEquals(bottom, "#MAGA")

    def test_short_last_sentence(self):
        '''if the last sentence is short, it should always be the
        second in the split'''

        tweet = "Met with @RepCummings today at the @WhiteHouse. Great discussion!"

        (top, bottom) = zendtrump.split_tweet(tweet)

        self.assertEquals(top, "Met with @RepCummings today at the @WhiteHouse")
        self.assertEquals(bottom, "Great discussion!")

if __name__ == '__main__':
    unittest.main()
