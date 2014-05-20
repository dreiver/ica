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
		raise Exception("Api requires the 'simplejson' library")

log = logging.getLogger(__name__)


@decorator
def api(func, *args, **kwargs):
	data   = None
	format = args[1]

	user = request.environ.get('REMOTE_USER', '')
	# If user not exist return forbidden
	if not user:
		data = response_error( 33 )
	
	"""
	# Create custom variables for current method
	if request.method == 'POST':
		response.status_code = 201 # The POST request if was successful must return '201 Created'
		c.post = {}
		for k, v in request.POST.iteritems():
			c.post[k] = v
	elif request.method == 'GET':
		c.get = {}
		for k, v in request.GET.iteritems():
			c.get[k] = v
	"""

	# If data has not been altered, then it is a right request
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

	response.int = html[code]
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
