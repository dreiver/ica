import os
from paste.script.command import Command
from paste.deploy import appconfig
from pylons import config
from ica.config.environment import load_environment


class ICACommand(Command):
    """Base class for commands"""
    group_name = 'ica'
    conf = appconfig('config:development.ini', relative_to='.')
    load_environment(conf.global_conf, conf.local_conf)


class RedisDB(ICACommand):
    usage = ''
    parser = Command.standard_parser(verbose=False)
    summary = 'Manage redis db instances'

    parser.add_option('-l', '--list', dest='list',
        action='store_true', default=False, help='list redis instances')

    parser.add_option('-c', '--cli', dest='cli',
        action='store_true', default=False, help='send command to arg passed redis instance')

    def command(self):
        cmd = self.args
        opt = vars(self.options)
        
        if opt['list'] is True:
            print 'list redis databases'
            return

        if len(cmd) != 2:
            print self.parser.format_help()
            return

        print cmd
        redis_instance = cmd[0]
        redis_command = cmd[1]

        """
        import pprint
        print "Hello, app script world!"
        print
        print "My options are:"
        print "    ", pprint.pformat(vars(self.options))
        print "My args are:"
        print "    ", pprint.pformat(self.args)
        print
        print "My parser help is:"
        print
        print self.parser.format_help()
        """


class UserManage(ICACommand):
    usage = ''
    parser = Command.standard_parser(verbose=False)
    summary = 'Manage users'

    parser.add_option('-l', '--list', dest='list',
        action='store_true', default=False, help='list users')

    parser.add_option('-u', '--user USERNAME', dest='prop',
        action='store_true', default=False, help='shows user properties')

    parser.add_option('-a', '--add USERNAME [FIELD1=VALUE1 FIELD2=VALUE2 ...]', dest='add',
        action='store_true', default=False, help='add a user (prompts for password if not supplied)\
        Field can be: apikey, password, email')

    parser.add_option('-p', '--passwd USERNAME', dest='passwd',
        action='store_true', default=False, help='set user password (prompts)')

    parser.add_option('-r', '--remove USERNAME', dest='remove',
        action='store_true', default=False, help='remove')

    max_args = None
    min_args = 0

    def command(self):
        
        if not self.args:
            self.list()
        else:
            cmd = self.args[0]
            opt = vars(self.options)

            if opt['add'] is True:
                self.add()
            elif opt['prop'] is True:
                self.prop()
            elif opt['passwd'] is True:
                self.passwd()
            elif opt['remove'] is True:
                self.remove(cmd)
            else:
                print self.parser.format_help()
                return

    def get_user_str(self, user):
        formatted = 'user_name=\'%s\''  % user.user_name
        formatted += ' display_name=\'%s\'' % user.display_name
        return formatted

    def list(self):
        from ica.model import User, Session
        
        print 'Users:'
        users = Session.query(User.user_name, User.display_name).order_by(User.user_id)
        print 'users = %i' % users.count()
        for user in users:
            print self.get_user_str(user)

    def add(self):
        print 'add user'

    def prop(self):
        print 'property user'

    def passwd(self):
        from ica.model import User, Session

        if (len(self.args) < 1 or len(self.args) > 2):
            print self.parser.format_help()
            return

        userparam = self.args[0]
        passwd = self.args[1]

        user = User.by_user_name(userparam)

        if user is None:
            print 'User not found \'%s\'' % userparam
            return

        print('Editing user: %s' % user.user_name)

        #print user
        #print passwd 
        #print 'set password user'

    def remove(self, cmd):
        print 'remove user '+cmd