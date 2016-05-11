#Uses Firebase to store data. The database will store data in the following format in json
#Hashtag
#   TweetID


from firebase import firebase
firebase = firebase.FirebaseApplication('https://unicode.firebaseio.com/', None)

tweetIDs = []
tweetIDsUP = []

def initTweetDB():
    pract = firebase.put('/', "ex", {'TweetID': [0, 1, 2]})
    print pract
    
#A function to append a new tweet's data to the database, using the above format for json.
#Simple function that takes in the hashtag in question and the tweetID associated with it.
#This function puts that data straight into the database.
def addTweetToDB(hashtag, tweetID):
    tweetIDs = firebase.get('/', hashtag)
    print tweetIDs
    if tweetIDs != None:
        tweetIDs['TweetID'].append(tweetID)
        print tweetIDs
        tweetIDsUP = tweetIDs['TweetID']
        found = False
        for x in range(0,len(tweetIDs)):
            if tweetID == tweetIDs[x]:
                found = True
        if found == False:
            result = firebase.put('/', hashtag, {'TweetID': tweetIDsUP})

        #print result
    else:
        tweetIDsUP.append(tweetID)
        result = firebase.put('/', hashtag, {'TweetID': tweetIDs})
        print result
    
    
#A function to grab the list of tweet IDs from the database for a given hashtag.
def getTweetIDs(hashtag):
    tweetIDs = firebase.get('/', hashtag)
    print tweetIDs['TweetID']
    return tweetIDs['TweetID']

#A function to record what questions users have already completed.
def recordQonUser(sessionID, tweetID):
    tweetIDs = firebase.get('/users', sessionID)
    print tweetIDs
    if tweetIDs != None:
        tweetIDs['TweetID'].append(tweetID)
        print tweetIDs
        tweetIDsUP = tweetIDs['TweetID']
        result = firebase.put('/users', sessionID, {'TweetID': tweetIDsUP})
        print result
    else:
        tweetIDsUP.append(tweetID)
        result = firebase.put('/users', sessionID, {'TweetID': tweetIDs})
        print result

#TestData
#initTweetDB()

#addTweetToDB("HackBCUHack", 910)

#getTweetIDs("HackBCUHack")
