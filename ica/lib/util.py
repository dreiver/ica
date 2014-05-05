import logging

from pylons import request, response, session, tmpl_context as c, url
from ica.lib.base import render

log = logging.getLogger(__name__)


def pjax(template):
	"""Determine whether the request was made by PJAX."""
	#if "X-PJAX" in request.headers:
	#	return render('metis/'+template)

	c.template = 'metis/'+template
	return render('metis/base.html')