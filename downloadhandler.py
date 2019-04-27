import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self):
		photo_key = self.request.get("key")
		if not blobstore.get(photo_key):
			pass
		else:
			self.send_blob(photo_key)

