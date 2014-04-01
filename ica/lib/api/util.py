import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.decorators.util import get_pylons
from paste.httpexceptions import get_exception
from decorator import decorator
from dicttoxml import dicttoxml as xml

try:
	import json
except ImportError:
	try:
		import simplejson as json
	except ImportError:
		raise Exception("App requires the 'simplejson' library")

log = logging.getLogger(__name__)


@decorator
def api(func, *args, **kwargs):
	data 		= None
	format      = args[1]
	token 		= args[2]
	secret		= None

	if token:
		if request.method == 'POST':
			c.post = {}
			for k, v in request.POST.iteritems():
				c.post[k] = v

			if not 'SECRET-TOKEN' in c.post:
				data = response_error( 64 )
			else:
				secret = c.post['SECRET-TOKEN']

		elif request.method == 'GET':
			c.get = {}
			for k, v in request.GET.iteritems():
				c.get[k] = v

			if not 'secret_token' in c.get:
				data = response_error( 64 )
			else:
				secret = c.get['secret_token']

	# If data has not been altered, then is a correct request
	if data is None:
		data = func(*args, **kwargs)

	if format == 'xml':
		response.headers['Content-Type'] = 'application/xml; charset=utf-8'
		resp = xml(data)
	else:
		response.headers['Content-Type'] = 'application/json; charset=utf-8'
		resp = json.dumps(data)

	return resp+'\n'


def response_error(code, headers=None):

	html = {
		32:400,
		33:401,
		34:404,
		44:405,
		64:403,
		88:402,
		89:406,
		92:500,
		130:503,
	}

	if headers:
		response.headerlist += headers

	response.status_code = html[code]
	result = { 'errors':
				[
					{
					'title':get_exception( html[code] ).title, 
					'message':get_exception( html[code] ).explanation,
					'code': code 
					}
				]
			}
	return result
