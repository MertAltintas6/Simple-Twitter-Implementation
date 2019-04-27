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

class Profile(webapp2.RequestHandler):

	def get(self):
		self.response.headers['Content-Type'] = 'text/html'

		user = users.get_current_user()		
		control = False

		if user == None:
			template_values = {'login_url':users.create_login_url(self.request.uri)}
			template = JINJA_ENVIRONMENT.get_template('landingPage.html')
			self.response.write(template.render(template_values))
			return
		
		myuser_key = ndb.Key('MyUser',user.user_id())
		myuser = myuser_key.get()

		username = self.request.get("username")

		if username == myuser.username:
			control=True

		profile_user_k = ndb.Key("AllUsers", username)
		the_user_key = profile_user_k.get()
		profile_user_key = ndb.Key("MyUser",the_user_key.userkey)
		profile_user = profile_user_key.get()
		
		t = Tweets()
		tweets = t.getTweetsByKey(profile_user)
		
		tweet_keys = myuser.tweetsList
		tweet_keys.reverse()

		if user.user_id() in profile_user.fallowersList:
			buttonValue = "Unfollow"
		else:
			buttonValue = "Follow"

		template_values = {'username':myuser.username, 'logout_url':users.create_logout_url(self.request.uri), 'tweet_keys': tweet_keys ,'profile_user':profile_user, 'tweets':tweets, 'buttonValue': buttonValue,'control':control,'fallowers_count':len(profile_user.fallowersList), 'fallowing_count': len(profile_user.fallowedList)}
		template = JINJA_ENVIRONMENT.get_template('profile.html')
		self.response.write(template.render(template_values))


	def post(self):
		self.response.headers['Content-Type'] = 'text/html'

		user = users.get_current_user()
		myuser_key = ndb.Key('MyUser',user.user_id())
		myuser = myuser_key.get()

		username = self.request.get("username")
		profile_user_k = ndb.Key("AllUsers", username)
		the_user_key = profile_user_k.get()
		profile_user_key = ndb.Key("MyUser",the_user_key.userkey)
		profile_user = profile_user_key.get()

		button = self.request.get("button")

		if button == "Follow":
			profile_user.fallowersList.append(user.user_id())
			myuser.fallowedList.append(the_user_key.userkey)
			myuser.put()
			profile_user.put()

		elif button == "Unfollow":
			profile_user.fallowersList.remove(user.user_id())
			myuser.fallowedList.remove(the_user_key.userkey)
			myuser.put()
			profile_user.put() 

		elif button == "Delete":
			tweetId = self.request.get("tweetId")
			myuser.tweetsList.remove(tweetId)
			myuser.tweet_count = len(myuser.tweetsList)
			tweet_key = ndb.Key('Tweets',tweetId)
			tweet = tweet_key.get()
			tweet.key.delete()
			myuser.put()

		redirect_url = '/profile?username=' + str(profile_user.username)
		self.redirect(redirect_url)


