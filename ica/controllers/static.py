import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from ica.lib.base import BaseController, render

log = logging.getLogger(__name__)

class StaticController(BaseController):

    def offline(self):
    	return render('metis/offline.html')
    	
    def constructing(self):
    	return render('metis/constructing.html')