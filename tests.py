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

        self.assertEquals(top, "hello")
        self.assertEquals(bottom, "world")

    def test_long_simple_split(self):
        '''simple split should work for long sentences too'''

        tweet = "LinkedIn Workforce Report: January and February were the strongest \
consecutive months for hiring since August and September 2015"

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

        tweet = "Met with @RepCummings today at the @WhiteHouse. Great discussion"

        (top, bottom) = zendtrump.split_tweet(tweet)

        self.assertEquals(top, "Met with @RepCummings today at the @WhiteHouse.")
        self.assertEquals(bottom, "Great discussion")

    def test_powerful_ending(self):
        '''if the last sentence ends in an exclamation mark,
        it's the second in the split'''

        tweet = "122 vicious prisoners, released by the Obama \
Administration from Gitmo, have returned to the battlefield. \
Just another terrible decision!"

        (top, bottom) = zendtrump.split_tweet(tweet)

        self.assertEquals(top, "122 vicious prisoners, released by the Obama \
Administration from Gitmo, have returned to the battlefield.")
        self.assertEquals(bottom, "Just another terrible decision!")

    def test_long_multi_sentence(self):
        ''''''

        tweet = "We are making great progress with healthcare. \
ObamaCare is imploding and will only get worse. \
Republicans coming together to get job done!"

        (top, bottom) = zendtrump.split_tweet(tweet)

        self.assertEquals(top, "We are making great progress with healthcare. \
ObamaCare is imploding and will only get worse.")
        self.assertEquals(bottom, "Republicans coming together to get job done!")


if __name__ == '__main__':
    unittest.main()

