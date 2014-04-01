import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from ica.lib.base import BaseController
from ica.lib.util import pjax
from pylons import app_globals as g
from datetime import datetime, timedelta

log = logging.getLogger(__name__)


class MainController(BaseController):


	def __before__(self):

		if not session.get('logged_in'):
			log.debug('Request received without a valid session')
			redirect('/login')

		if g.test_redis(g.redis_ica):
			redirect('/offline')

		c.session_name   = session['name']
		c.session_user   = session['user']
		c.session_role   = session['role']
		c.session_access = datetime.strptime(session['access'], '%Y-%m-%d %H:%M:%S.%f').strftime('%e %b %H:%M')

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
					{'title': 'Precargada', 'href': '/constructing', 'icon': 'icon-angle-right' },
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

		c.menu[0]['status'] = 'active'
		c.title      	    = c.menu[0]['title']
		c.title_icon 	    = c.menu[0]['icon']

		c.ica_logs_error     = g.redis_ica.llen('ica:logs:error')
		c.ica_logs_calls     = g.redis_ica.llen('ica:logs:calls')
		c.ica_logs_warning   = g.redis_ica.llen('ica:logs:warning')
		c.ica_logs_serv_jpos = g.redis_ica.llen('ica:logs:serv:jpos')#CABAL

		c.day_values = g.get_day_values(g.redis_ica)
		c.day_calls  = g.get_day_calls(g.redis_ica)

		c.week        = g.get_week(g.redis_ica)
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

		c.menu[4]['status'] = 'active'
		c.title             = c.menu[4]['title']+" / "+c.menu[4]['child'][0]['title']
		c.title_icon        = c.menu[4]['icon']

		c.ica_logs_error     = g.redis_ica.lrange('ica:logs:error', 0 , 4)
		c.ica_logs_warning   = g.redis_ica.lrange('ica:logs:warning', 0 , 4)
		c.ica_logs_serv_jpos = g.redis_ica.lrange('ica:logs:cabal:jpos', 0 , 4)#CABAL

		users   = g.redis_ica.lrange('ica:users', 0 , -1)
		c.users = []

		for i in users:
			user           = g.redis_ica.hgetall('ica:user:'+i)
			user['expire'] = g.redis_ica.ttl('ica:user:'+i+':keyexpire')
			expire         = datetime.now() + timedelta( seconds=user['expire'] )
			user['ttl']    = expire.strftime('%e %b %H:%M')
			user['access'] = datetime.strptime(user['access'], '%Y-%m-%d %H:%M:%S.%f').strftime('%e %b %H:%M')
			user['user']   = i
			c.users.append(user)

		return pjax('panel.html')


	def currentcalls(self):

		c.menu[3]['status'] = 'active'
		c.title             = c.menu[3]['title']+" / "+c.menu[3]['child'][0]['title']
		c.title_icon        = c.menu[3]['icon']

		return pjax('currentcalls.html')


	#######################
	# CUSTOM CLIENT CABAL #
	#######################
	def bines(self):
		c.menu[2]['status'] = 'active'
		c.title             = c.menu[2]['title']+" / "+c.menu[2]['child'][0]['title']
		c.title_icon        = c.menu[2]['icon']

		return pjax('cabal-bines.html')

