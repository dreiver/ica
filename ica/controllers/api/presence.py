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


class PresenceController(BaseController):
	
	@api
	def presence(self, format, credentials=False, method='POST'):
		data = { 'caca': [] }
		return (data)
