import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from string import punctuation
import os

from myuser import MyUser
from tweet import Tweets
from allUsers import AllUsers

JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True)

class tweetEdit(webapp2.RequestHandler):
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
				template_values = {'logout_url':users.create_logout_url(self.request.uri)}
				template = JINJA_ENVIRONMENT.get_template('firstLogin.html')
				self.response.write(template.render(template_values))
				return
			else:
				tweetId = self.request.get("id")
				tweet_key = ndb.Key('Tweets', tweetId)
				tweet = tweet_key.get()
				template_values = {'myuser':myuser,'tweet':tweet}
				template = JINJA_ENVIRONMENT.get_template('tweetEdit.html')
				self.response.write(template.render(template_values))
				return


	def post(self):
		button = self.request.get("button")
		user = users.get_current_user()
		myuser_key = ndb.Key('MyUser',user.user_id())
		myuser = myuser_key.get()

		if button == "Submit":
			tweetId = self.request.get("id")
			tweet_key = ndb.Key('Tweets', tweetId)
			tweet = tweet_key.get()
			
			tweetText = self.request.get("tweet")
			tweet.tweetText = tweetText
			tweet.tweetWords = self.strip_punctuation(tweetText)
			tweet.put()
			
			redirect_url = '/profile?username=' + str(tweet.username)
			self.redirect(redirect_url)