import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from ica.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AccessController(BaseController):


	def login(self):
		# If session exist, not need login
		if session.get('logged_in'):
			redirect('/')
		#log.debug("Login session request")
		return render('metis/login.html')


	def logout(self):
		session.clear()
		session.save()
		log.debug("Session destroy request")
		redirect('/login')


	def changepasswd(self, user):
		c.changepasswd_user  = user
		c.changepasswd_alert = 1
		return render('metis/changepasswd.html')