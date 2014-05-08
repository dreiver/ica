import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import app_globals as g

from ica.lib.base import BaseController, render
from ica.lib.util import test_redis

from datetime import datetime, timedelta
import hashlib
import base64

log = logging.getLogger(__name__)


class AccessController(BaseController):

	def __before__(self):
		if request.method == 'POST':
			c.post = {}
			for k, v in request.POST.iteritems():
				c.post[k] = v

			if test_redis(g.redis_ica):
				redirect('/offline')


	def logout(self):
		session.clear()
		session.save()
		log.debug('Session destroy request')
		redirect('/login')


	def login(self):
		# If session exist, not need login
		if session.get('logged_in'):
			redirect('/')

		if request.method == 'GET':
			return render('metis/login.html')

		# If post data not exist, return error
		if not ('username' in c.post and 'password' in c.post and 'action' in c.post):
			c.login_error = True
		else:
			if g.redis_ica.hget('ica:user:'+c.post['username'], 'password') == hashlib.sha1( c.post['password'] ).hexdigest():
				# Get user current data
				login = g.redis_ica.hgetall('ica:user:'+c.post['username'])

				# If is the first login or has expired, is time for create a new password
				if (login['access'] == '' or not g.redis_ica.exists('ica:user:'+c.post['username']+':keyexpire') ):
					redirect('/changepasswd/user/'+c.post['username'])

				session['user']      = c.post['username']
				session['role']      = login['role']
				session['name']      = login['name']
				session['access']    = login['access']
				session['logged_in'] = True
				session.save()

				redirect('/')
			else:
				log.warning("Login attempt failed from '%s' user '%s' action 'login'", request.environ['REMOTE_ADDR'], c.post['username'])
				c.login_error = True

		return render('metis/login.html')


	def changepasswd(self, user):
		c.changepasswd_user  = user
		c.changepasswd_alert = 1

		if request.method == 'GET':
			return render('metis/changepasswd.html')

		# If post data not exist, return error
		if not ('username' in c.post and 'password' in c.post and 'action' in c.post and 'passwordnew' in c.post and 'passwordconfirm' in c.post):
			c.changepasswd_error = True
		else:
			if g.redis_ica.hget('ica:user:'+c.post['username'], 'password') == hashlib.sha1( c.post['password'] ).hexdigest():

				if (c.post['passwordnew'] == c.post['passwordconfirm'] and c.post['password'] != c.post['passwordnew']):

					token_basic_old = g.redis_ica.hget('ica:user:'+c.post['username'], 'token_basic')
					token_basic_new = base64.b64encode( c.post['username']+':'+c.post['passwordnew'] )
					
					# Set the pipeline method
					pipe = g.redis_ica.pipeline()
					pipe.hset('ica:user:'+c.post['username'], 'password', hashlib.sha1( c.post['passwordnew'] ).hexdigest())
					pipe.hset('ica:user:'+c.post['username'], 'passwordsip', hashlib.md5( c.post['username']+':ICA:'+c.post['passwordnew'] ).hexdigest())
					pipe.hset('ica:user:'+c.post['username'], 'access', datetime.now())
					pipe.hset('ica:user:'+c.post['username'], 'token_basic', token_basic_new)
					pipe.incr('ica:user:'+c.post['username']+':keyexpire')
					pipe.expireat('ica:user:'+c.post['username']+':keyexpire', datetime.now() + timedelta(days=20) )
					pipe.hset('ica:users:token:basic', token_basic_new , c.post['username'])
					
					if token_basic_old:
						pipe.hdel('ica:users:token:basic', token_basic_old)

					# Write data
					pipe.execute()

					# Get user current data
					login = g.redis_ica.hgetall('ica:user:'+c.post['username'])

					session['user']      = c.post['username']
					session['role']      = login['role']
					session['name']      = login['name']
					session['access']    = login['access']
					session['logged_in'] = True
					session.save()

					redirect('/')
				else:
					c.changepasswd_error = True
			else:
				log.warning("Login attempt failed from '%s' user '%s' action 'changepasswd'", request.environ['REMOTE_ADDR'], c.post['username'])
				c.changepasswd_error = True

		return render('metis/changepasswd.html')
