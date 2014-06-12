"""The base Controller API

Provides the BaseController class for subclassing.
"""
import logging
import time

from pylons import request, response, session, tmpl_context as c
from pylons.controllers import WSGIController
from pylons.templating import render_jinja2 as render

log = logging.getLogger(__name__)

class BaseController(WSGIController):

    def __init__(self):
    	c.timer = time.time()


    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        return WSGIController.__call__(self, environ, start_response)


    def __after__(self, environ):
    	end_timer = time.time() - c.timer
    	url = environ['PATH_INFO']
    	log.info("'%s' render time %.3f seconds" % (url, end_timer))
