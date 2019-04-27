#Tweets Class
from google.appengine.ext import ndb
from string import punctuation

class Tweets(ndb.Model):
	tweetText = ndb.StringProperty()
	username = ndb.StringProperty()
	tweetWords = ndb.StringProperty(repeated=True)
	timestamp = ndb.DateTimeProperty(auto_now = True)
	blobKey = ndb.BlobKeyProperty()

	def strip_punctuation(self, s):
		s = s.lower()
		clean = ''.join(c for c in s if c not in punctuation)
		words = clean.split()
		return words

	def getTweetsByKey(self,myuser):
		tweets = []
		for key in myuser.tweetsList:
			tweet_key = ndb.Key('Tweets',key)
			tweet = tweet_key.get()
			tweets.append(tweet)
		tweets.reverse()
		return tweets[0:50]

	def getTweets(self,myuser):
		tweets = []
		usernames = self.getUsernames(myuser)
		tweets = Tweets.query(Tweets.username.IN(usernames)).order(-Tweets.timestamp).fetch(50)
		return tweets

	def getUsernames(self, myuser):
		usernames = []
		usernames.append(myuser.username)
		if myuser.fallowedList != None:
			for key in myuser.fallowedList:
				u_key = ndb.Key("MyUser",key)
				u = u_key.get()
				usernames.append(u.username)

		return usernames