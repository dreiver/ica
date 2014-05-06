"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    # import controllers here rather than at root level because
    # pylons config is initialised by this point.

    # Helpers to reduce code clutter
    GET = dict(method=['GET'])
    PUT = dict(method=['PUT'])
    POST = dict(method=['POST'])
    DELETE = dict(method=['DELETE'])
    GET_POST = dict(method=['GET', 'POST'])
    PUT_POST = dict(method=['PUT', 'POST'])
    PUT_POST_DELETE = dict(method=['PUT', 'POST', 'DELETE'])
    OPTIONS = dict(method=['OPTIONS'])

    map = Mapper(directory=config['pylons.paths']['controllers'],
                always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    #######
    # API #
    #######
    #Conf
    map.connect('/api/v1/conf/index{.format:json|xml}', controller='api', action='conf')
    map.connect('/api/v1/conf/trunk{.format:json|xml}', controller='api', action='trunk')
    #Graph
    map.connect('/api/v1/graph/last_week{.format:json|xml}', controller='api', action='last_week')
    #Calls
    #map.connect('/api/v1/calls/currentcalls{.format:json|xml}', controller='api', action='currentcalls')
    #VOIP
    #map.connect('/api/v1/voip/presence{.format:json|xml}', controller='api/presence', action='presence', conditions=dict(method=["POST"]))
    #map.resource('voip', 'voip/sip', controller='api/comments', path_prefix='/api/v1', name_prefix='api_')

    ############
    # /END API #
    ############

    ########
    # Main #
    ########

    # Index
    map.connect('index', '/', controller='main', action='index')
    map.connect('index', '/index', controller='main', action='index')
    
    # Voip
    map.connect('/voip/sip', controller='main', action='sip')
    map.connect('/voip/iax', controller='main', action='iax')
    
    # Reports
    map.connect('/reports/currentcalls', controller='main', action='currentcalls')
    map.connect('/reports/general', controller='main', action='general')
    map.connect('/reports/graphs', controller='main', action='graphs')
    map.connect('/reports/calls', controller='main', action='calls')
    
    # System
    map.connect('/system/panel', controller='main', action='panel')
    map.connect('/system/panel/{alert}', controller='main', action='alert')
    map.connect('/system/settings', controller='main', action='settings')

    # Login / Logout
    map.connect('/login', controller='access', action='login')
    map.connect('/logout', controller='access', action='logout')
    map.connect('/changepasswd/user/{user}', controller='access', action='changepasswd')
    
    # Static
    map.connect('/offline', controller='static',  action='static')

    #############
    # /END MAIN #
    #############

    #######################
    # CUSTOM CLIENT CABAL #
    #######################
    map.connect('/cabal/bines', controller='main', action='bines')#CABAL
    #map.connect('/cabal/consultas', controller='main', action='consultas')#CABAL
    map.connect('/cabal/precargada', controller='main', action='precargada')#CABAL
    #map.connect('/cabal/autorizaciones', controller='main', action='autorizaciones')#CABAL

    ############################
    # /END CUSTOM CLIENT CABAL #
    ############################

    return map
