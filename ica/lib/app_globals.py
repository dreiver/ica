"""The application's Globals object"""
import logging

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from pylons.controllers.util import abort, redirect

try:
	import redis as redis
except ImportError:
	raise Exception("Cache backend requires the 'redis' library")

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
        self.redis_voip = redis.Redis( host=config['redis.voip_host'], port=int(config['redis.voip_port']), socket_timeout=int(config['redis.voip_timeout']) )
        self.redis_ica  = redis.Redis( host=config['redis.ica_host'], port=int(config['redis.ica_port']), socket_timeout=int(config['redis.ica_timeout']) )
        self.template = config['ica.template']
