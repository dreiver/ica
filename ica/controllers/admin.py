import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons import app_globals as g
from pylons.controllers.util import abort, redirect

from ica.lib.base import BaseController
from ica.lib.util import *
from datetime import datetime, timedelta
from pylons.i18n import get_lang, set_lang

log = logging.getLogger(__name__)


class AdminController(BaseController):

	def index(self):
		return 'index in development'

	def users(self):
		return 'users in development'
