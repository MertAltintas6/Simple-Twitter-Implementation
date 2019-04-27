from google.appengine.ext import ndb

class AllUsers(ndb.Model):
	userkey = ndb.StringProperty()