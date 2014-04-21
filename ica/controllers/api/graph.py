import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons import app_globals as g
from pylons import config

from ica.lib.base import BaseController
from ica.lib.api.util import api

log = logging.getLogger(__name__)


class GraphController(BaseController):
	
	@api
	def last_week(self, format='json'):
		data = { 'label': '', 'data': [] }
		week = g.get_week(g.redis_ica)

		for i in week:
			day = int(i['days'].strftime('%s')) * 1000
			data['data'].append([ day, i['calls'] ])

		return (data)