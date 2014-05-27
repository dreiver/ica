import os
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import app_globals as g

from ica.lib.base import BaseController, render
from ica.lib.util import test_redis
from ica.lib.helpers import flash

from ica.model import User, Session

from datetime import datetime, timedelta
import hashlib
import base64

log = logging.getLogger(__name__)


class AccessController(BaseController):

	def login(self):
		login_counter = request.environ['repoze.who.logins']

		if login_counter > 0:
			c.login_error = True

		c.login_counter = login_counter
		c.came_from = request.params.get('came_from') or url('/')
		
		return render('metis/login.html')
		
	def logged_in(self):
		identity = request.environ.get('repoze.who.identity')
		came_from = str(request.params.get('came_from', '')) or url('/')
		
		if not identity:
			login_counter = request.environ['repoze.who.logins'] + 1
			redirect(url('/login', came_from=came_from, __logins=login_counter))
		else:
			user = User.by_user_name('eslovelle')
			if 'mail' in identity:
				user.email_address = identity['mail'][0]
			if 'cn' in identity:
				user.display_name = identity['cn'][0]
			Session.commit()

			"""
			metadata = request.environ['repoze.who.identity']
			print dict(metadata=metadata.items())
			"""

		redirect(came_from)

	def logged_out(self):
		redirect('/')
