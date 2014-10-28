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
    map.connect('profile', '/profile', controller='main', action='profile', conditions=GET)

    # Profile
    with map.submapper(path_prefix='/profile', controller='main', conditions=GET) as m:
        m.connect('profile', '/account', action='account')
        m.connect('profile', '/notifications', action='notifications')
        m.connect('profile', '/design', action='design')
        m.connect('profile', '/support', action='support')
        m.connect('profile', '/reset_private_token', action='reset_private_token', conditions=POST)
    
    # Voip
    with map.submapper(path_prefix='/voip', controller='main', conditions=GET) as m:
        m.connect('voip', '/sip', action='sip')
        m.connect('voip', '/iax', action='iax')
        m.connect('voip', '/sms', action='sms')
        m.connect('voip', '/pstn', action='pstn')
        m.connect('voip', '/media', action='media')
        m.connect('voip', '/dialer', action='dialer')
        
    
    # Reports
    with map.submapper(path_prefix='/reports', controller='main', conditions=GET) as m:
        m.connect('reports', '/currentcalls', action='currentcalls')
        m.connect('reports', '/general', action='general')
        m.connect('reports', '/detailed', action='detailed')
        
    
    # System
    with map.submapper(path_prefix='/system', controller='main', conditions=GET) as m:
        m.connect('system', '/panel', action='panel')
        m.connect('system', '/panel/{alert}', action='alert', requirements={"alert": "error|warning|jpos"})
        m.connect('system', '/settings', action='settings')

    # Admin
    with map.submapper(path_prefix='/admin', controller='admin', conditions=GET) as m:
        m.connect('admin', '/users', action='users')

    # Login / Logout
    #with map.submapper(controller='access', conditions=GET) as m:
    with map.submapper(controller='access') as m:
        m.connect('access', '/login', action='login')
        m.connect('access', '/user/logged_in', action='logged_in')
        m.connect('access', '/user/logged_out', action='logged_out')
    
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