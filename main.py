import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
import os
import time 

from blobcollection import BlobCollection
from myuser import MyUser
from tweet import Tweets
from allUsers import AllUsers
from FirstLogin import FirstLogin
from edit import Edit
from profile import Profile
from tweetEdit import tweetEdit
from uploadhandler import UploadHandler
from downloadhandler import DownloadHandler

JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True)

class MainPage(webapp2.RequestHandler):

	def get(self):
		self.response.headers['Content-Type'] = 'text/html'

		user = users.get_current_user()		
		myuser = None

		if user == None:
			template_values = {'login_url':users.create_login_url(self.request.uri)}
			template = JINJA_ENVIRONMENT.get_template('landingPage.html')
			self.response.write(template.render(template_values))
			return

		else:
			myuser_key = ndb.Key('MyUser', user.user_id())
			myuser = myuser_key.get()
			#FirstLogin
			if myuser == None:
				self.redirect('/firstLogin')
				return
			#Not the first login
			t = Tweets()
			tweets = t.getTweets(myuser)
			template_values = {'logout_url':users.create_logout_url(self.request.uri),'upload_url':blobstore.create_upload_url('/upload'), 'myuser': myuser, 'tweets': tweets,'fallowers_count':len(myuser.fallowersList), 'fallowing_count': len(myuser.fallowedList)}
			template = JINJA_ENVIRONMENT.get_template('mainpage.html')
			self.response.write(template.render(template_values))


	def post(self):

		user = users.get_current_user()
		myuser_key = ndb.Key('MyUser', user.user_id())
		myuser = myuser_key.get()

		button = self.request.get("button")

		if button == "Search":
			text = self.request.get("username").strip().lower()
			t = Tweets()
			textWords = t.strip_punctuation(text)
			retrieved_users = []
			retrieved_tweets = []
			retrieved_user = None
			
			for word in set(textWords):
				DB_user_key = ndb.Key('AllUsers',word)
				DB_user = DB_user_key.get()		
				if DB_user:
					retrieved_user_key = ndb.Key('MyUser',DB_user.userkey)
					retrieved_user = retrieved_user_key.get()
					retrieved_users.append(retrieved_user.username)

			retrieved_tweet_keys = Tweets.query(Tweets.tweetWords.IN(textWords)).fetch(keys_only=True)

			for key in retrieved_tweet_keys:
					t = key.get()
					retrieved_tweets.append(t) 
			
			tweets = None
			template_values = {'logout_url':users.create_logout_url(self.request.uri), 'myuser': myuser, 'tweets': tweets, 'retrieved_users':retrieved_users,'retrieved_tweets':retrieved_tweets, 'fallowers_count':len(myuser.fallowersList), 'fallowing_count': len(myuser.fallowedList)}
			template = JINJA_ENVIRONMENT.get_template('mainpage.html')
			self.response.write(template.render(template_values))
				
			return

		self.redirect('/')


app = webapp2.WSGIApplication([
	('/', MainPage),
	('/firstLogin', FirstLogin),
	('/edit', Edit),
	('/profile', Profile),
	('/tweetEdit', tweetEdit),
	('/upload', UploadHandler),
	('/view_photo',DownloadHandler)], debug = True)