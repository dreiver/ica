import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons import app_globals as g
from ica.lib.base import render
from ica.model import User, Session
from datetime import datetime, timedelta
import time
import uuid

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise Exception("App requires the 'json' or 'simplejson' library")

log = logging.getLogger(__name__)


def pjax(template):
    """Determine whether the request was made by PJAX."""
    client = session.get('client_type')

    if ('preferred' in client or 'advanced' in client):
        if 'X-PJAX' in request.headers:
            return render(g.template+'/'+template)

    c.template = g.template+'/'+template
    return render(g.template+'/base.html')


def test_redis(redis):
    error = 0
    try:
        redis.ping()
    except Exception as error:
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

    return ','.join(values)


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


def get_user_by_user_name(login):
    return User.by_user_name(unicode(login))


def get_user_by_token(token):
    return User.by_token(unicode(token))


def get_user_by_extern_uid(extern_uid):
    return User.by_extern_uid(unicode(extern_uid))


def get_users_paginate(min=0, max=10):
    return Session.query(User.user_name, User.display_name).order_by(User.user_id).limit(max).offset(min).all()


def update_settings(username, profile):
    user = User.by_user_name(unicode(username))
    user.display_name = profile.get('user_name')
    user.email_address = profile.get('email_address')
    #user.company = profile.get('user_company')
    #user.location = profile.get('user_location')
    set_session_vars(user)
    Session.commit()


def update_private_token(user_name):
    token = create_private_token()
    Session.query(User).filter(User.user_name==user_name).update({'token': unicode(token)})
    Session.commit()
    return token


def create_private_token():
    u = uuid.uuid4()
    return u.bytes.encode('base64')[:20]


def add_new_user(login, password, provider, extern_uid=None, client_type=None):
    token = create_private_token()
    user = User(user_name=login, password=password, token=token, provider=provider, extern_uid=extern_uid, client_type=client_type)
    Session.add(user)
    Session.commit()


def set_session_vars(user):
    session['user_name'] = user.user_name
    session['mail'] = user.email_address
    session['name'] = user.display_name
    session['created'] = user.created
    session['token'] = user.token
    session['theme'] = user.theme
    session['provider'] = user.provider
    session['client_type'] = user.client_type
    session.save()

def ica_app_settings(request, session):
    identity = request.environ.get('repoze.who.identity')

    # User session settings
    c.name = session.get('user_name')
    c.mail = session.get('mail')
    c.name = session.get('name')
    c.token = session.get('token')
    c.theme = session.get('theme')
    c.created = session.get('created').strftime('%e %b %Y')
    c.provider = session.get('provider')
    c.last_login = datetime.fromtimestamp(session.get('_accessed_time')).strftime('%e %b %H:%M')

    # Aplication settings
    c.pjax = "data-pjax='#main-content'"
    client = session.get('client_type')
    c.keys = {}
    c.keys['settings'] = 'ica:users:%s:settings' %(session['user_name'])

    if 'ldap_attributes' in request.environ['repoze.who.plugins']:
        ldap_attributes = request.environ.get('ica.ldap_attributes')
        c.identity = {}

        for i in ldap_attributes:
            if i in identity:
                c.identity[i] = identity.get(i)[0].decode('utf-8')

    #if c.ajax is True:
    if ('preferred' in client or 'advanced' in client):
        c.ajax = True
        c.head_style = "display: none;"


def update_user_identity(identity, provider):

    if provider == 'ldap':
        user = get_user_by_extern_uid( identity['repoze.who.userid'] )
    else:
        user = get_user_by_user_name( identity['repoze.who.userid'] )

    if user is None:
        log.error('Unexpected, user must be added in previous stept')
        return None
        
    """
    login = identity['userdata'].split('|')
    user = get_user_by_user_name(login[0])

    if user is None:
        add_new_user(login[0], login[1])
        user = get_user_by_user_name(login[0])

    #user.password = login[1]

    """
    
    if 'mail' in identity:
        user.email_address = identity['mail'][0]
    if 'cn' in identity:
        user.display_name = identity['cn'][0]
    #if 'repoze.who.userid' in identity:
    #    user.extern_uid = identity['repoze.who.userid']
    if user.theme is None:
        user.theme = g.template

    set_session_vars(user)

    Session.commit()
