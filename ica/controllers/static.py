import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import app_globals as g

from ica.lib.base import BaseController, render

log = logging.getLogger(__name__)

class StaticController(BaseController):

    def offline(self):
    	return render(g.template+'/offline.html')
    	
    def constructing(self):
    	return render(g.template+'/constructing.html')