import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from string import punctuation
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
	def strip_punctuation(self, s):
		s = s.lower()
		clean = ''.join(c for c in s if c not in punctuation)
		words = clean.split()
		return words

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
			tweets = self.getTweets(myuser)
			template_values = {'logout_url':users.create_logout_url(self.request.uri),'upload_url':blobstore.create_upload_url('/upload'), 'myuser': myuser, 'tweets': tweets,'fallowers_count':len(myuser.fallowersList), 'fallowing_count': len(myuser.fallowedList)}
			template = JINJA_ENVIRONMENT.get_template('mainpage.html')
			self.response.write(template.render(template_values))


	def post(self):

		user = users.get_current_user()
		myuser_key = ndb.Key('MyUser', user.user_id())
		myuser = myuser_key.get()

		button = self.request.get("button")

		#if button == "Tweet":
		#	tweetText = self.request.get("tweet")
		#	myuser.tweet_count += 1
		#	tweetKey = user.user_id() + ":" + str(myuser.tweet_count)
		#	tweetWords = self.strip_punctuation(tweetText)
		#	tweet = Tweets(id=tweetKey, username = myuser.username, tweetText=tweetText, tweetWords=tweetWords)
		#	myuser.tweetsList.append(tweetKey)
			
		#	tweet.put()
		#	myuser.put()
		#	time.sleep(0.05)

		if button == "Search":
			text = self.request.get("username").strip().lower()
			textWords = self.strip_punctuation(text)
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

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/firstLogin', FirstLogin),
	('/edit', Edit),
	('/profile', Profile),
	('/tweetEdit', tweetEdit),
	('/upload', UploadHandler),
	('/view_photo',DownloadHandler)], debug = True)