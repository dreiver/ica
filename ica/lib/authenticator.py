import logging

from paste.deploy.converters import asbool
from zope.interface import implements
from repoze.who.interfaces import IAuthenticator

from ica.model import User, Session

from ica.plugins.auth_ldap import (
    LDAPAttributesPlugin, LDAPAuthenticatorPlugin, LDAPSearchAuthenticatorPlugin
)
import ldap

log = logging.getLogger(__name__)


class UsernamePasswordAuthenticator(object):
    implements(IAuthenticator)

    def authenticate(self, environ, identity):
        if not ('login' in identity and 'password' in identity):
            return None

        login = identity['login']
        user = User.by_user_name(login)

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
class ReconnectingAuthenticatorPlugin(LDAPSearchAuthenticatorPlugin):
    implements(IAuthenticator)

    def __init__(self, *args, **kw):
        self.ldap = kw
        super(ReconnectingAuthenticatorPlugin, self).__init__(*args, **kw)


    def authenticate(self, environ, identity):
        res = None
        print self.ldap
        if asbool(self.ldap['ldap_enabled']):
            res = super(LDAPSearchAuthenticatorPlugin, self).authenticate(environ, identity)



        return res
"""