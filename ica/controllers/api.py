import logging

from pylons import app_globals as g
from pylons import config

from ica.lib.base import BaseController
from ica.lib.util import get_week
from ica.lib.api import api
import json

log = logging.getLogger(__name__)


class ApiController(BaseController):

	@api
	def conf(self, format='json'):
		data = {
			'socket_server': config['ica.socket_server'],
			'socket_port': config['ica.socket_port'],
			'domain': config['ica.domain'],
			'debug': config['debug'] }

		return (data)


	@api
	def trunk(self, format='json'):
		data = { 'trunks': 0, 'servers': 0 }

		for i in g.redis_ica.keys('ica:trunks:*'):
			data['trunks']  += int(g.redis_ica.get(i))
			data['servers'] += 1

		return (data)


	@api
	def last_week(self, format='json'):
		data = { 'label': '', 'data': [] }
		week = get_week(g.redis_ica)

		for i in week:
			day = int(i['days'].strftime('%s')) * 1000
			data['data'].append([ day, i['calls'] ])

		return (data)


	@api
	def currentcalls(self, format, credentials=True, method='GET'):
		data = { 'data': [] }

		for i in g.redis_ica.lrange('ica:logs:calls', 0 , -1):
			data['data'].append( json.loads(i) )

		return (data)