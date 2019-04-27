from google.appengine.ext import ndb


class BlobCollection(ndb.Model):
	filename = ndb.StringProperty()
	blob = ndb.BlobKeyProperty()