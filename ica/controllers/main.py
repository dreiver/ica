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

		if not request.environ.get('repoze.who.identity'):
			redirect('/login')

		if test_redis(g.redis_ica):
			redirect('/offline')

		#if 'ldap_auth' in request.environ['repoze.who.plugins']:

		#print request.environ['repoze.who.identity'].items()
		#metadata = request.environ['repoze.who.identity']['mail']
		#print dict(metadata=metadata.items())

		#c.session_name   = session['name']
		#c.session_mail   = session['mail']
		#c.session_user   = session['user']
		#c.session_role_i = session['role']
		#c.session_role   = role_name(session['role'])
		#c.session_access = datetime.strptime(session['access'], '%Y-%m-%d %H:%M:%S.%f').strftime('%e %b %H:%M')

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

	def index(self):
		#c.menu[0]['status'] = 'active'
		#c.title      	    = c.menu[0]['title']
		#c.title_icon 	    = c.menu[0]['icon']

		c.ica_logs_error     = g.redis_ica.llen('ica:logs:error')
		c.ica_logs_calls     = g.redis_ica.llen('ica:logs:calls')
		c.ica_logs_warning   = g.redis_ica.llen('ica:logs:warning')
		c.ica_logs_serv_jpos = g.redis_ica.llen('ica:logs:serv:jpos')#CABAL

		c.day_values = get_day_values(g.redis_ica)
		c.day_calls  = get_day_calls(g.redis_ica)

		c.week        = get_week(g.redis_ica)
		c.week_calls  = 0
		c.week_values = []
		
		for i in c.week:
			c.week_calls += int( i['calls'] )
			c.week_values.append( str(i['calls']) )

		c.week_values = ','.join(c.week_values)

		c.month_values = '0,0,0,0,0,0,0,0,0,0,0,0'
		c.month_calls  = '0'
		
		return pjax('index.html')


	def panel(self):
		#c.menu[4]['status'] = 'active'
		#c.title             = c.menu[4]['title']+" / "+c.menu[4]['child'][0]['title']
		#c.title_icon        = c.menu[4]['icon']

		c.ica_logs_error     = g.redis_ica.lrange('ica:logs:error', 0, 4)
		c.ica_logs_warning   = g.redis_ica.lrange('ica:logs:warning', 0, 4)
		c.ica_logs_serv_jpos = g.redis_ica.lrange('ica:logs:cabal:jpos', 0, 4)#CABAL

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

		return pjax('system-panel.html')

	def alert(self, alert):

		if alert == 'error':
			key 	 = 'ica:logs:error'
			c.type   = 'important'
			c.action = 'error'

		elif alert == 'warning':
			key 	 = 'ica:logs:warning'
			c.type   = 'warning'
			c.action = 'warning'

		elif alert == 'jpos':#CABAL
			key 	 = 'ica:logs:jpos'
			c.type   = 'important'
			c.action = 'error'

		c.alert  = g.redis_ica.lrange(key, 0, -1)

		return pjax('system-panel-alert.html')


	def currentcalls(self):
		#c.menu[3]['status'] = 'active'
		#c.title             = c.menu[3]['title']+" / "+c.menu[3]['child'][0]['title']
		#c.title_icon        = c.menu[3]['icon']

		return pjax('currentcalls.html')


	#######################
	# CUSTOM CLIENT CABAL #
	#######################
	def bines(self):
		#c.menu[2]['status'] = 'active'
		#c.title             = c.menu[2]['title']+" / "+c.menu[2]['child'][0]['title']
		#c.title_icon        = c.menu[2]['icon']

		return pjax('cabal-bines.html')

	def precargada(self):

		c.prod    = []
		c.preprod = []
		c.voice   = g.redis_voip.lrange('ivr:cabal:precargada:voice', 0, -1)
		c.bines   = g.redis_voip.lrange('ivr:cabal:precargada:bines', 0, -1)

		prod    = g.redis_voip.lrange('ivr:cabal:prod:precargada:extension', 0, -1)
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
