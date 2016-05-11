from twython import Twython
import re

class Questions(object):
    
    def __init__(self, appKey, appKeySecret, accessToken, accessTokenSecret):
        
        self.questions = {}
        self.handle = Twython(app_key=appKey, app_secret=appKeySecret, oauth_token=accessToken, oauth_token_secret=accessTokenSecret)
        
        self.handle.get_home_timeline()
        print "Remaining API calls: ", self.handle.get_lastfunction_header('x-rate-limit-remaining')

        
    def getTweet(self, tweetId):
        status = self.handle.show_status(id=tweetId)
        tweetText = self.unescape(status['text'])
        tweetText = re.sub(r'([ \t]*[#]+[\w]+[ \t]*|[ \t]*[#]+[ \t]*|[ \t]+$|[ \t]*[@]\w+[ \t]*)', '', tweetText)
        return tweetText
    
    def exprValidator(self, tweetId):
        
        text = self.getTweet(tweetId)
        
        print "validation: " + text
        
        if text[-1] in ['>', '<']:
            text = text[:-1]
        elif text[-2] in ['>','<','=','!']:
            text = text[:-2]
        else:
            return False
        
        try:
            exec("r = " + text)
            if r == None:
                return False
            return True
        except:
            return False

    def refresh(self, channel):
        search = self.handle.search(q=channel, count=25)
        tweets = search['statuses']

        for tweet in tweets:
            # Not a retweet
            if tweet['text'][:2] != 'RT' and self.exprValidator(tweet['id']):
                #db.addTweetToDB(channel, tweet['id'])
                # If channel exists
                if channel in self.questions:
                    # If ID is not on the list
                    if tweet['id'] not in self.questions[channel]:
                        self.questions[channel].append(tweet['id'])
                # Channel doesn't exist, create it
                else:
                    self.questions[channel] = [ tweet['id'] ]
    
    def unescape(self, text):
        text = text.replace("&lt;", "<")
        text = text.replace("&gt;", ">")
        text = text.replace("&amp;", "&")
        return text
                    
# if __name__ == '__main__':
    
    # CattleOfRa API keys
    # TWITTER_APP_KEY = 'Xn1CSR611kD5jjrcANQScEwXp'
    # TWITTER_APP_KEY_SECRET = 'cVE72wv6t5wybGRfmrnMyAK5KPBozKdbKeO9Zy1J2EzvcHqBjx' 
    # TWITTER_ACCESS_TOKEN = '4450140375-8cKMsHGdNntCHJyqBkp6ahvIkd4mBqaCF3siewP'
    # TWITTER_ACCESS_TOKEN_SECRET = 'gWSLhlNKlcw8WmVkpR3IeOUHrHawlwDUgTlveJ7rkW8DC'
    
    # TWITTER_APP_KEY = '9TVKbuMJW89bt62Nm28vmXYF3'
    # TWITTER_APP_KEY_SECRET = '2Yo6u7mcQwgL9XtesHj18vGr9ImuIwt2kPmFHEyaWdOtE7BEqj' 
    # TWITTER_ACCESS_TOKEN = '4074464595-H3KNJfiiigV36zJye7mZ6F4HN0Tgo0OxeZjbPmo'
    # TWITTER_ACCESS_TOKEN_SECRET = 'Cli93wY4hChWewTXFMW49rZJQY0ybOSSReMSI2lVtR9lZ'
    # 
    # setOfQuestions = Questions(TWITTER_APP_KEY, TWITTER_APP_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    # 
    # setOfQuestions.refresh("#hackbcuhack")
    # print setOfQuestions.questions
    # for question in setOfQuestions.questions["#hackbcuhack"]:
    #     print setOfQuestions.getTweet(question)
        
