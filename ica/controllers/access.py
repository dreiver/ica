import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import app_globals as g

from ica.lib.base import BaseController, render
from ica.lib.util import test_redis, update_user_identity
from ica.lib.helpers import flash

from datetime import datetime, timedelta
import hashlib
import base64

log = logging.getLogger(__name__)


class AccessController(BaseController):

	def login(self):
		c.auth = 'custom'
		identity = request.environ.get('repoze.who.identity')
		login_counter = request.environ['repoze.who.logins']

		if identity:
			redirect('/')
		
		if 'ldap_auth' in request.environ['repoze.who.plugins']:
			c.auth = 'ldap'
			c.ldap_enabled = True

		if login_counter > 0:
			c.login_error = True

		c.login_counter = login_counter
		c.came_from = request.params.get('came_from') or url('/')
		
		return render(g.template+'/login.html')
		
	def logged_in(self):
		identity = request.environ.get('repoze.who.identity')
		came_from = str(request.params.get('came_from', '')) or url('/')
		
		if not identity:
			login_counter = request.environ['repoze.who.logins'] + 1
			redirect(url('/login', came_from=came_from, __logins=login_counter))
		else:
			provider = request.environ.get('ica.login.auth')
			update_user_identity(identity, provider)

		redirect(came_from)

	def logged_out(self):
		session.clear()
		session.save()
		redirect('/')
