#User class 
from google.appengine.ext import ndb

class MyUser(ndb.Model):
	name = ndb.StringProperty()
	username = ndb.StringProperty()
	profileDesc = ndb.StringProperty()
	tweetsList = ndb.StringProperty(repeated=True)
	fallowersList = ndb.StringProperty(repeated=True)
	fallowedList = ndb.StringProperty(repeated=True)
	tweet_count = ndb.IntegerProperty()



