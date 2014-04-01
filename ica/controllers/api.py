import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import app_globals as g
from pylons import config

from ica.lib.base import BaseController
from ica.lib.api.util import api, response_error

from datetime import datetime, timedelta
import hashlib

log = logging.getLogger(__name__)


class ApiController(BaseController):
	
	@api
	def conf(self, format, credentials=True, method='GET'):
		data = {
			'socket_server': config['socket_server'],
			'socket_port': config['socket_port'],
			'domain': config['domain'],
			'debug': config['debug'] }

		return (data)


	@api
	def trunks(self, format, credentials=True, method='GET'):
		data = { 'trunks': 0, 'servers': 0 }

		for i in g.redis_ica.keys('ica:trunks:*'):
			data['trunks']  += int(g.redis_ica.get(i))
			data['servers'] += 1

		return (data)


	@api
	def week_graph(self, format, credentials=True, method='GET'):
		data = { 'label': '', 'data': [] }
		week = g.get_week(g.redis_ica)

		for i in week:
			day = int(i['days'].strftime('%s')) * 1000
			data['data'].append([ day, i['calls'] ])

		return (data)


	@api
	def currentcalls(self, format, credentials=True, method='GET'):
		data = { 'data': [] }

		for i in g.redis_ica.lrange('ica:logs:calls', 0 , -1):
			data['data'].append( g.json.loads(i) )

		return (data)


	@api
	def presence(self, format, credentials=False, method='POST'):
		data = { 'caca': [] }
		return (data)


	@api
	def login(self, format, credentials=False, method='POST'):	
		# If post data not exist, return error
		if (not c.post['username'] or not c.post['password'] or not c.post['action']):
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
	def changepasswd(self, format, credentials=False, method='POST'):
		# If post data not exist, return error
		if (not c.post['username'] or not c.post['password'] or not c.post['action'] or not c.post['passwordnew'] or not c.post['passwordconfirm']):
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