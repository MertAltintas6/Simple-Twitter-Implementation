from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
from string import punctuation
import time


from myuser import MyUser
from tweet import Tweets
from allUsers import AllUsers
from blobcollection import BlobCollection

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def strip_punctuation(self, s):
		s = s.lower()
		clean = ''.join(c for c in s if c not in punctuation)
		words = clean.split()
		return words

	def post(self):
		user = users.get_current_user()
		myuser_key = ndb.Key('MyUser',user.user_id())
		myuser = myuser_key.get()
		tweetId = user.user_id() + ":" + str(myuser.tweet_count+1)
		success = False
		try:
			upload = self.get_uploads()[0]

			blobinfo = blobstore.BlobInfo(upload.key())
			filename = blobinfo.filename

			new_blob = BlobCollection(id=tweetId, filename= filename, blob=upload.key())
			new_blob.put()
			success = True
			
		except Exception as e:
			pass

		tweetText = self.request.get("tweet")
		myuser.tweet_count += 1
		tweetWords = self.strip_punctuation(tweetText)
		if success:
			tweet = Tweets(id=tweetId, username = myuser.username, tweetText=tweetText, tweetWords=tweetWords, blobKey=new_blob.blob)
		else:
			tweet = Tweets(id=tweetId, username = myuser.username, tweetText=tweetText, tweetWords=tweetWords)

		myuser.tweetsList.append(tweetId)
			
		tweet.put()
		myuser.put()
		time.sleep(0.05)

		self.redirect('/')