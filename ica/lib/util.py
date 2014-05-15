import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons import app_globals as g
from ica.lib.base import render
from datetime import datetime, timedelta
import time

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise Exception("App requires the 'simplejson' library")

log = logging.getLogger(__name__)


def pjax(template):
	"""Determine whether the request was made by PJAX."""
	#if "X-PJAX" in request.headers:
	#	return render('metis/'+template)

	c.template = 'metis/'+template
	return render('metis/base.html')


def test_redis(redis):
    error = 0
    try:
        redis.ping()
    except redis.ConnectionError, error:
        log.error(error)
    
    return (error)


def get_day_calls(redis):
    return int(redis.llen('ica:reports:calls:day:'+datetime.now().strftime('%d%m%Y')))


def get_day_values(redis):
    values     = []
    day_hours  = {}
    day_values = redis.lrange('ica:reports:calls:day:'+datetime.now().strftime('%d%m%Y'), 0, -1)

    for i in day_values:
        uid  = json.loads(i)['uid'].split('.')[0]
        hour = time.strftime('%H', time.gmtime(int(uid)))
        day_hours[hour] = day_hours.get(hour, 0) + 1

    for i in range(3,24):
        if day_hours.get(str(i)) == None: value = 0
        else: value = day_hours.get(str(i))
        values.append(str(value))

    return ",".join(values)


def get_week(redis):
    week  = []

    for i in range(0, 7):
        day  = datetime.now() - timedelta(days=i)
        llen = redis.llen('ica:reports:calls:day:'+day.strftime('%d%m%Y'))
        week.append( { 'calls': llen, 'days': day } )

    return week


def role_name(role):
    if int(role) == 1:
        return 'Administrador'
    elif int(role) == 2:
        return 'Moderador'
    else:
        return 'Usuario'