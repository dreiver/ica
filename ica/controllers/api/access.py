import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import app_globals as g
from pylons import config

from ica.lib.base import BaseController
from ica.lib.api.util import api, response_error

from datetime import datetime, timedelta
import hashlib
import base64

log = logging.getLogger(__name__)


class AccessController(BaseController):

	@api
	def login(self, format='json', token=True):
		# If post data not exist, return error
		if (not 'username' in c.post or not 'password' in c.post or not 'action' in c.post):
			return (response_error( 32 ))

		# If session exist, not need login
		if session.get('logged_in'):
			return ({ 'succes': { 'type':'login', 'message':'redirect', 'destination': '/', 'code':0 } })

		if g.redis_ica.hget('ica:user:'+c.post['username'], 'password') == hashlib.sha1( c.post['password'] ).hexdigest():
			# Get user current data
			login = g.redis_ica.hgetall('ica:user:'+c.post['username'])

			# If is the first login or has expired, is time for create a new password
			if (login['access'] == '' or not g.redis_ica.exists('ica:user:'+c.post['username']+':keyexpire') ):
				return ({ 'succes': { 'type':'login', 'message':'redirect', 'destination': '/changepasswd/user/'+c.post['username'], 'code':0 } })

			session['user']      = c.post['username']
			session['role']      = login['role']
			session['name']      = login['name']
			session['access']    = login['access']
			session['logged_in'] = True
			session.save()

			return ({ 'succes': { 'type':'login', 'message':'successfull', 'code':1 } })
		else:
			log.warning("Login attempt failed from '%s' user '%s' action 'login'", request.environ['REMOTE_ADDR'], c.post['username'])
			return ({ 'succes': { 'type':'login', 'message':'invalid credentials', 'code':0 } })


	@api
	def changepasswd(self, format='json', token=True):
		# If post data not exist, return error
		if (not 'username' in c.post or not 'password' in c.post or not 'action' in c.post\
			or not 'passwordnew' in c.post or not 'passwordconfirm' in c.post):
			return (response_error( 32 ))
			
		if g.redis_ica.hget('ica:user:'+c.post['username'], 'password') == hashlib.sha1( c.post['password'] ).hexdigest():
			# Set the pipeline method
			pipe = g.redis_ica.pipeline()

			if (c.post['passwordnew'] == c.post['passwordconfirm'] and c.post['password'] != c.post['passwordnew']):
				pipe.hset('ica:user:'+c.post['username'], 'password', hashlib.sha1( c.post['passwordnew'] ).hexdigest())
				pipe.hset('ica:user:'+c.post['username'], 'passwordsip', hashlib.md5( c.post['username']+':ICA:'+c.post['passwordnew'] ).hexdigest())
				pipe.hset('ica:user:'+c.post['username'], 'access', datetime.now())
				pipe.incr('ica:user:'+c.post['username']+':keyexpire')
				pipe.expireat('ica:user:'+c.post['username']+':keyexpire', datetime.now() + timedelta(days=20) )

				# Write data
				pipe.execute()

				return ({ 'succes': { 'type':'changepasswd', 'message':'successfull', 'code':1 } })
			else:
				return ({ 'succes': { 'type':'changepasswd', 'message':'invalid credentials or password mismatch', 'code':0 } })
		else:
			log.warning("Login attempt failed from '%s' user '%s' action 'changepasswd'", request.environ['REMOTE_ADDR'], c.post['username'])
			return ({ 'succes': { 'type':'login', 'message':'invalid credentials', 'code':0 } })