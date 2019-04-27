import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from tweet import Tweets
from allUsers import AllUsers

JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True)

class FirstLogin(webapp2.RequestHandler):
	
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
				self.redirect('/')
				return


	def post(self):
		button = self.request.get("button")
		user = users.get_current_user()
		myuser = None
		emptyList = []
		if button == "Next":
			username = self.request.get("username").strip().lower()
			DB_user_key = ndb.Key('AllUsers', username)
			DB_user = DB_user_key.get()

			if DB_user == None:
				myuser = MyUser(id=user.user_id(),name="", username=username,profileDesc="", tweetsList = emptyList,fallowersList = emptyList, fallowedList = emptyList, tweet_count = len(emptyList))
				myuser.put()
				DB_user = AllUsers(id=username, userkey = user.user_id())
				DB_user.put()
				self.redirect('edit')
				return

			else:
				#this username is taken 
				self.redirect('/firstLogin')

			
