"""The application's Globals object"""
import logging

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from pylons.controllers.util import abort, redirect
from datetime import datetime, timedelta
import time

try:
	import redis as redis
except ImportError:
	raise Exception("Cache backend requires the 'redis' library")

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise Exception("App requires the 'simplejson' library")

log = logging.getLogger(__name__)

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    def __init__(self, config):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        self.cache = CacheManager(**parse_cache_config_options(config))
        self.redis = redis
        self.json  = json
        self.redis_voip = redis.Redis( host=config['voip_host'], port=int(config['voip_port']), socket_timeout=int(config['voip_timeout']) )
        self.redis_ica  = redis.Redis( host=config['ica_host'], port=int(config['ica_port']), socket_timeout=int(config['ica_timeout']) )


    def test_redis(self, redis):
        error = 0
        try:
            redis.ping()
        except self.redis.ConnectionError, error:
            log.error(error)
        
        return (error)


    def get_day_calls(self, redis):
        return int(redis.llen("ica:reports:calls:day:"+datetime.now().strftime('%d%m%Y')))


    def get_day_values(self, redis):
        values     = []
        day_hours  = {}
        day_values = redis.lrange("ica:reports:calls:day:"+datetime.now().strftime('%d%m%Y'), 0, -1)

        for i in day_values:
            uid  = json.loads(i)['uid'].split(".")[0]
            hour = time.strftime("%H", time.gmtime(int(uid)))
            day_hours[hour] = day_hours.get(hour, 0) + 1

        for i in range(3,24):
            if day_hours.get(str(i)) == None: value = 0
            else: value = day_hours.get(str(i))
            values.append(str(value))

        return ",".join(values)


    def get_week(self, redis):
        week  = []

        for i in range(0, 7):
            day  = datetime.now() - timedelta(days=i)
            llen = redis.llen("ica:reports:calls:day:"+day.strftime('%d%m%Y'))
            week.append( { 'calls': llen, 'days': day } )

        return week
