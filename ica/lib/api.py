import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons import config
from pylons.decorators.util import get_pylons
from paste.httpexceptions import get_exception
from decorator import decorator
from dicttoxml import dicttoxml as xml
from ica.lib.util import get_user_by_token

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
	user   = None
	token  = None
	format = args[1]

	token_header_name = config.get('api.token_header_name', 'Authorization')
	api_token = request.headers.get(token_header_name, '').split(' ')

	# Credentials via header
	if len(api_token) == 2:
		if (api_token[0] == 'token' and len(api_token[1]) == 20):
			token = api_token[1]
		elif (api_token[0] != 'Basic'):
			data = response_error( 32 )
	
	# Credentials via parameter
	elif len(request.params) == 1:
		if 'access_token' in request.params:
			token = request.params.getall('access_token')[0]
			if len(token) != 20:
				data = response_error( 32 )
		else:
			data = response_error( 32 )

	# No Authentication
	#else:
	#	data = response_error( 33 )


	if token:
		user = get_user_by_token(token)
	else:
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
		33:403,
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
