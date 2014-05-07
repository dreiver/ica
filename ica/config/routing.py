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

    with map.submapper(path_prefix='/api{ver:/v1|}', controller='api', conditions=GET) as m:
        m.connect('api', '/conf/index{.format:json|xml}', action='conf')
        m.connect('api', '/conf/trunk{.format:json|xml}', action='trunk')
        m.connect('api', '/graph/last_week{.format:json|xml}', action='last_week')
        m.connect('api', '/calls/currentcalls{.format:json|xml}', action='currentcalls')
    #map.resource('voip', 'voip/sip', controller='api/comments', path_prefix='/api/v1', name_prefix='CACA_')

    ############
    # /END API #
    ############

    ########
    # Main #
    ########

    # Index
    map.connect('index', '/', controller='main', action='index', conditions=GET)
    map.connect('index', '/index', controller='main', action='index', conditions=GET)
    
    # Voip
    with map.submapper(path_prefix='/voip', controller='main', conditions=GET) as m:
        m.connect('voip', '/sip', action='sip')
        m.connect('voip', '/iax', action='iax')
    
    # Reports
    with map.submapper(path_prefix='/reports', controller='main', conditions=GET) as m:
        m.connect('reports', '/currentcalls', action='currentcalls')
        m.connect('reports', '/general', action='general')
        m.connect('reports', '/graphs', action='graphs')
        m.connect('reports', '/calls', action='calls')
    
    # System
    with map.submapper(path_prefix='/system', controller='main', conditions=GET) as m:
        m.connect('system', '/panel', action='panel')
        m.connect('system', '/panel/{alert}', action='alert', requirements={"alert": "error|warning|jpos"})
        m.connect('system', '/settings', action='settings')

    # Admin
    with map.submapper(path_prefix='/admin', controller='admin', conditions=GET) as m:
        m.connect('admin', '/users', action='users')
        m.connect('admin', '/databases', action='databases')

    # Login / Logout
    with map.submapper(controller='access', conditions=GET) as m:
        m.connect('access', '/login', action='login', conditions=GET_POST)
        m.connect('access', '/logout', action='logout')
        m.connect('access', '/changepasswd/user/{user}', action='changepasswd', conditions=GET_POST)
    
    # Static
    with map.submapper(controller='static', conditions=GET) as m:
        m.connect('static', '/offline', action='offline')
        m.connect('static', '/constructing', action='constructing')

    #############
    # /END MAIN #
    #############

    #######################
    # CUSTOM CLIENT CABAL #
    #######################

    with map.submapper(controller='main', conditions=GET) as m:
        m.connect('cabal', '/cabal/bines', action='bines')
        m.connect('cabal', '/cabal/consultas', action='consultas')
        m.connect('cabal', '/cabal/precargada', action='precargada')
        m.connect('cabal', '/cabal/autorizaciones', action='autorizaciones')

    ############################
    # /END CUSTOM CLIENT CABAL #
    ############################

    return map