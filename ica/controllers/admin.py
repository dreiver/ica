import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from ica.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AdminController(BaseController):

    def users(self):
        return 'Hello World users'
