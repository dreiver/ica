import logging

from zope.interface import implements
from repoze.who.interfaces import IAuthenticator

from ica.lib.util import get_user_by_user_name, add_new_user

log = logging.getLogger(__name__)

class UsernamePasswordAuthenticator(object):
    implements(IAuthenticator)

    def authenticate(self, environ, identity):
        if not ('login' in identity and 'password' in identity):
            return None

        # Check if ldap plugin is enabled and the user has valid credentials
        """
        if 'ldap_auth' in environ['repoze.who.plugins'] and \
            not 'repoze.who.userid' in identity:
            return None
        """

        # Store user|password
        auth = environ.get('ica.login.auth', 'custom')

        if ('ldap' in auth and not 'repoze.who.userid' in identity):
            return None

        user = get_user_by_user_name(identity['login'])

        if user is None:
            if 'repoze.who.userid' in identity:
                add_new_user(identity['login'], identity['password'], auth, identity['repoze.who.userid'])
            else:
                return None

        #Not working!
        if user:
            user.password = identity['password']

        """
        #TODO:
        if 'HTTP_AUTHORIZATION' in environ or \
            not 'ldap_auth' in environ['repoze.who.plugins'] or \
            'custom' in auth:
            
            user = get_user_by_user_name(identity['login'])
            
            # If login was ok and user not exist, create it
            if 'repoze.who.userid' in identity and \
                user is None:
                add_new_user(identity['login'], identity['password'])

            #if not 'ldap_auth' in environ['repoze.who.plugins']:
            #    if user:
            #        print identity
            #        return str(identity['login'])

        """
        
        """
        if user is None:
            log.debug('Login failed - username \'%s\' not found', login)
        elif not user.is_active():
            log.debug('Login as \'%s\' failed - user isn\'t active', login)
        elif not user.validate_password(identity['password']):
            log.debug('Login as \'%s\' failed - password not valid', login)
        else:
            return user.name

        return None
        """
        
