import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons import app_globals as g
from pylons.controllers.util import abort, redirect

from ica.lib.base import BaseController
from ica.lib.util import *
from datetime import datetime, timedelta

log = logging.getLogger(__name__)


class MainController(BaseController):

	def __before__(self):

		identity = request.environ.get('repoze.who.identity')

		if not identity:
			redirect('/login')

		if test_redis(g.redis_ica):
			redirect('/offline')

		# User session settings
		c.name = session.get('user_name')
		c.mail = session.get('mail')
		c.name = session.get('name')
		c.token = session.get('token')
		c.theme = session.get('theme')
		c.created = session.get('created').strftime('%e %b %Y')
		c.provider = session.get('provider')
		c.last_login = datetime.fromtimestamp(session.get('_accessed_time')).strftime('%e %b %H:%M')
		
		# Aplication settings
		client = session.get('client_type')

		if 'ldap_attributes' in request.environ['repoze.who.plugins']:
			ldap_attributes = request.environ.get('ica.ldap_attributes')
			c.identity = {}

			for i in ldap_attributes:
				if i in identity:
					c.identity[i] = identity.get(i)[0].decode('utf-8')

		#if c.ajax is True:
		if ('preferred' in client or 'advanced' in client):
			c.ajax = True
			c.head_style = "display: none;"

		"""
		conf_menu = [
			{ 'title': 'Home', 'icon': 'icon-home', 'href': '/index' },
			{ 'title': 'Voip', 'icon': 'icon-headphones', 'child': 
				[
					{'title': 'SIP', 'icon': 'icon-angle-right', 'href': '/constructing'},
					{'title': 'IAX', 'icon': 'icon-angle-right', 'href': '/constructing'},
					{'title': 'PSTN', 'icon': 'icon-angle-right', 'href': '/constructing'},
				] 
			},
			{ 'title': 'Cabal', 'icon': 'icon-sitemap', 'child': 
				[
					{'title': 'ABM bines', 'href': '/cabal/bines', 'icon': 'icon-list-ol' },
					{'title': 'Precargada', 'href': '/cabal/precargada', 'icon': 'icon-angle-right' },
					{'title': 'Autorizaciones', 'href': '/constructing', 'icon': 'icon-angle-right' },
					{'title': 'Consultas', 'href': '/constructing', 'icon': 'icon-angle-right' },
				]
			},
			{ 'title': 'Reports', 'icon': 'icon-bar-chart', 'child':
				[
					{'title': 'Current Calls', 'href': '/reports/currentcalls', 'icon': 'icon-phone-sign' },
					{'title': 'General', 'href': '/constructing', 'icon': 'icon-angle-right' },
					{'title': 'Calls', 'href': '/constructing', 'icon': 'icon-angle-right' },
					{'title': 'Graphs', 'href': '/constructing', 'icon': 'icon-angle-right' },
				]
			},
			{ 'title': 'System', 'icon': 'icon-cogs', 'child':
				[
					{ 'title': 'Panel', 'icon': 'icon-tasks', 'href': '/system/panel' },
					{ 'title': 'Application Settings', 'icon': 'icon-wrench', 'href': '/constructing' },
				]
			},
		]

		c.menu = conf_menu
		"""

	#####################
	# Index / Dashboard #
	#####################

	def index(self):

		c.ica_logs_error = g.redis_ica.llen('ica:logs:error')
		c.ica_logs_calls = g.redis_ica.llen('ica:logs:calls')
		c.ica_logs_warning = g.redis_ica.llen('ica:logs:warning')
		c.ica_logs_serv_jpos = g.redis_ica.llen('ica:logs:serv:jpos')#CABAL

		c.day_values = get_day_values(g.redis_ica)
		c.day_calls = get_day_calls(g.redis_ica)

		c.week = get_week(g.redis_ica)
		c.week_calls = 0
		c.week_values = []
		
		for i in c.week:
			c.week_calls += int( i['calls'] )
			c.week_values.append( str(i['calls']) )

		c.week_values = ','.join(c.week_values)

		c.month_values = '0,0,0,0,0,0,0,0,0,0,0,0'
		c.month_calls = '0'
		
		return pjax('index.html')


	def panel(self):

		c.ica_logs_error = g.redis_ica.lrange('ica:logs:error', 0, 4)
		c.ica_logs_warning = g.redis_ica.lrange('ica:logs:warning', 0, 4)
		c.ica_logs_serv_jpos = g.redis_ica.lrange('ica:logs:cabal:jpos', 0, 4)#CABAL

		c.users = get_users_paginate(0, 10)

		"""
		users   = g.redis_ica.smembers('ica:users')
		c.users = []

		for i in users:
			user           = g.redis_ica.hgetall('ica:user:'+i)
			user['expire'] = g.redis_ica.ttl('ica:user:'+i+':keyexpire')
			expire         = datetime.now() + timedelta( seconds=user['expire'] )
			user['ttl']    = expire.strftime('%e %b %H:%M')
			user['access'] = datetime.strptime(user['access'], '%Y-%m-%d %H:%M:%S.%f').strftime('%e %b %H:%M')
			user['role_n'] = role_name(user['role'])
			user['user']   = i
			c.users.append(user)
		"""

		return pjax('system-panel.html')

	def alert(self, alert):

		if alert == 'error':
			key = 'ica:logs:error'
			c.type = 'important'
			c.action = 'error'

		elif alert == 'warning':
			key = 'ica:logs:warning'
			c.type = 'warning'
			c.action = 'warning'

		elif alert == 'jpos':#CABAL
			key = 'ica:logs:jpos'
			c.type = 'important'
			c.action = 'error'

		c.alert = g.redis_ica.lrange(key, 0, -1)

		return pjax('system-panel-alert.html')


	def currentcalls(self):
		return pjax('currentcalls.html')


	###########
	# Profile #
	###########

	def profile(self):
		return pjax('profile.html')

	def account(self):
		return pjax('profile-account.html')

	def notifications(self):
		return pjax('profile-notifications.html')

	def design(self):
		return "design in development"

	def support(self):
		return "support in development"

	#######################
	# CUSTOM CLIENT CABAL #
	#######################
	def bines(self):
		return pjax('cabal-bines.html')


	def precargada(self):
		c.prod = []
		c.preprod = []
		c.voice = g.redis_voip.lrange('ivr:cabal:precargada:voice', 0, -1)
		c.bines = g.redis_voip.lrange('ivr:cabal:precargada:bines', 0, -1)

		prod = g.redis_voip.lrange('ivr:cabal:prod:precargada:extension', 0, -1)
		preprod = g.redis_voip.lrange('ivr:cabal:preprod:precargada:extension', 0, -1)

		for i in prod:
			this = g.redis_voip.hgetall('ivr:cabal:prod:precargada:'+i)
			this['extension'] = i
			c.prod.append(this)

		for i in preprod:
			this = g.redis_voip.hgetall('ivr:cabal:preprod:precargada:'+i)
			this['extension'] = i
			c.preprod.append(this)
		
		return pjax('cabal-precargada.html')
		