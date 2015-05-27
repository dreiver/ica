import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons import app_globals as g
from pylons.controllers.util import abort, redirect

from ica.lib.base import BaseController
from ica.lib.util import *
from datetime import datetime, timedelta
from pylons.i18n import get_lang, set_lang

from ica.model import User, Session

log = logging.getLogger(__name__)


class MainController(BaseController):

	def __before__(self):

		identity = request.environ.get('repoze.who.identity')

		if not identity:
			redirect('/login')

		if test_redis(g.redis_ica):
			redirect('/offline')

		ica_app_settings(request, session)

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


	##########
	# Search #
	##########
	def search(self):
		return "search in development"

	########
	# User #
	########

	def __get_username(self, user):
		if (len(user) < 4 or len(user) > 16):
			abort(404)

		u = User.by_user_name(unicode(user))

		if u is None:
			abort(404)

		return u

	def user(self, user):
		username = self.__get_username(user)
		return username.display_name+" in development"

	def stars(self, user):
		username = self.__get_username(username)
		return username.display_name+" starts in development"


	###########
	# Profile #
	###########

	def profile(self):
		return pjax('profile.html')

	def account(self):
		return pjax('profile-account.html')

	def notifications(self):
		c.notifications_global = g.redis_ica.hget(c.keys['settings'], 'notifications_global')
		c.notifications_messages = g.redis_ica.hget(c.keys['settings'], 'notifications_messages')
		c.notifications_missed_calls = g.redis_ica.hget(c.keys['settings'], 'notifications_missed_calls')
		return pjax('profile-notifications.html')

	def design(self):
		return "design in development"

	def support(self):
		return "support in development"

	def reset_private_token(self):
		session['token'] = update_private_token(session['user_name'])
		session.save()
		return session['token']

	def reset_password(self):
		#return "reset_password in development"
		redirect('/logout')

	def update_settings(self):
		profile = dict(request.POST)
		update_settings(session['user_name'], profile)
		return profile.get('user_name')

	def notifications_global(self):
		profile = dict(request.POST)

		if not 'notifications_global' in profile:
			return 'error'

		g.redis_ica.hset(c.keys['settings'], 'notifications_global', profile['notifications_global'])

		return profile['notifications_global']

	def notifications_level(self):
		notifications_level = dict(request.POST)

		if not ('action' in notifications_level and 'value' in notifications_level):
			return 'error'

		g.redis_ica.hset(c.keys['settings'], notifications_level['action'], notifications_level['value'])

		return notifications_level['action']


	###########
	# Reports #
	###########

	def general(self):
		return "general in development"

	def currentcalls(self):
		return "currentcalls in development"

	def detailed(self):
		return "detailed in development"


	########
	# Voip #
	########

	def sip(self):
		return "sip in development"

	def iax(self):
		return "iax in development"

	def sms(self):
		return "sms in development"

	def pstn(self):
		return "pstn in development"

	def media(self):
		return "media in development"

	def dialer(self):
		return "dialer in development"


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
		
