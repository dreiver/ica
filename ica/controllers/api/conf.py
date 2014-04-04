import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import app_globals as g
from pylons import config

from ica.lib.base import BaseController
from ica.lib.api.util import api, response_error

log = logging.getLogger(__name__)


class ConfController(BaseController):
	
	@api
	def index(self, format='json'):
		data = {
			'socket_server': config['socket_server'],
			'socket_port': config['socket_port'],
			'domain': config['domain'],
			'debug': config['debug'] }

		return (data)

	@api
	def trunk(self, format='json'):
		data = { 'trunks': 0, 'servers': 0 }

		for i in g.redis_ica.keys('ica:trunks:*'):
			data['trunks']  += int(g.redis_ica.get(i))
			data['servers'] += 1

		return (data)