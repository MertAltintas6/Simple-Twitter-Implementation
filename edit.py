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

class Edit(webapp2.RequestHandler):
	
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
				template_values = {'logout_url':users.create_logout_url(self.request.uri), 'myuser':myuser}
				template = JINJA_ENVIRONMENT.get_template('edit.html')
				self.response.write(template.render(template_values))
				return


	def post(self):
		button = self.request.get("button")
		user = users.get_current_user()
		myuser_key = ndb.Key('MyUser',user.user_id())
		myuser = myuser_key.get()

		if button == "Submit":
			myuser.name = self.request.get("name")
			myuser.profileDesc = self.request.get("profileDesc")
			myuser.put()
			redirect_url = '/profile?username=' + str(myuser.username)
			self.redirect(redirect_url)