from flask import render_template, Blueprint
import Questions
import DatabaseAccess as db
import unittest
import random

from flask import Flask

app = Flask(__name__)

userq = {}
#ques = {'1':'5**2 ==', '2':'[1,2,3,4,5][2] ==', '3':'5 + 5 ==', '4':'"hello".upper() ==', '5':'not (5 + 10 < 15) ==', '6':'len( [2, 0, 1, 6] ) =='}
ques = {}

#TWITTER_APP_KEY = '9TVKbuMJW89bt62Nm28vmXYF3'
#TWITTER_APP_KEY_SECRET = '2Yo6u7mcQwgL9XtesHj18vGr9ImuIwt2kPmFHEyaWdOtE7BEqj' 
#TWITTER_ACCESS_TOKEN = '4074464595-H3KNJfiiigV36zJye7mZ6F4HN0Tgo0OxeZjbPmo'
#TWITTER_ACCESS_TOKEN_SECRET = 'Cli93wY4hChWewTXFMW49rZJQY0ybOSSReMSI2lVtR9lZ'

# CattleOfRa API keys
TWITTER_APP_KEY = 'Xn1CSR611kD5jjrcANQScEwXp'
TWITTER_APP_KEY_SECRET = 'cVE72wv6t5wybGRfmrnMyAK5KPBozKdbKeO9Zy1J2EzvcHqBjx' 
TWITTER_ACCESS_TOKEN = '4450140375-8cKMsHGdNntCHJyqBkp6ahvIkd4mBqaCF3siewP'
TWITTER_ACCESS_TOKEN_SECRET = 'gWSLhlNKlcw8WmVkpR3IeOUHrHawlwDUgTlveJ7rkW8DC'

@app.route('/')
def hello_world():
    return render_template('index.html')
    
    
@app.route('/tag/<string:hashtag>')
def cpage(hashtag):
    twitter = Questions.Questions(TWITTER_APP_KEY, TWITTER_APP_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    #twitter.refresh('#' + hashtag)
    twitter.refresh(hashtag)
    print("twitter.questions" + str(twitter.questions))
    for question in twitter.questions[hashtag]:
        ques[str(question)] = twitter.getTweet(question)
    print ques
    return render_template('active.html', title = '#{}'.format(hashtag))

@app.route('/api/v1.0/getsid')
def get_sid():
    return "{}".format(random.randint(10000, 99999))


@app.route('/api/v1.0/getquestion/<data>', methods=['GET'])
def new_questions(data):
    sid, hash = data.split('^')
    a = '1'
    
    if sid in userq:
        qlist = [x for x in ques.keys() if x not in userq[sid]]
        if len(qlist) < 1:
            return "False"
        else:
            a = random.choice(qlist)  
    else:
        a = random.choice(ques.keys())

    return "{}^{}".format(a, ques[a])
    
    
@app.route('/api/v1.0/checkanswer/<data>', methods=['GET'])
def check_answer(data):
    sid, tweetid, answer = data.split('^')
    q = ques[tweetid]
    c = " "
    
    if q[-1] in ['<', '>']:
        c = q[-1]
        q = q[:-1]
    else:
        c = q[-2:]
        q = q[:-2]
        
    if q == answer:
        return "False"
    
    try:
        exec("a = " + q)
        exec("b = " + answer)
        if not str(a) == str(b):
            return "False"
    except:
        return "False"
    
    if sid in userq:
        userq[sid].append(tweetid)
    else:
        userq[sid] = [tweetid]

    print userq[sid]
    return "True"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
