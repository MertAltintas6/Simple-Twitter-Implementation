#Tweets Class
from google.appengine.ext import ndb

class Tweets(ndb.Model):
	tweetText = ndb.StringProperty()
	username = ndb.StringProperty()
	tweetWords = ndb.StringProperty(repeated=True)
	timestamp = ndb.DateTimeProperty(auto_now = True)
	blobKey = ndb.BlobKeyProperty()