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
            print 'in development'
            return

        if len(cmd) != 2:
            print self.parser.format_help()
            return

        print cmd
        redis_instance = cmd[0]
        redis_command = cmd[1]


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
        Field can be: user, password, email')

    parser.add_option('-p', '--passwd USERNAME', dest='passwd',
        action='store_true', default=False, help='set new user password (prompts)')

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

        print 'OK - Done'

    def add(self):
        from ica.model import User, Session
        from ica.lib.util import add_new_user

        if len(self.args) != 1:
            print self.parser.format_help()
            return

        username = self.args[0]
        password = self.passwd_cmd()

        if len(username) < 4:
            print 'ERR - User must have a min length of 5 characters'
            return

        if password is None:
            return

        user = User.by_user_name(unicode(username))
        if user is not None:
            print 'ERR - User allready exist into database'
            return

        add_new_user(username, password)

    def prop(self):
        from ica.model import User, Session
        print 'in development'

    def passwd_cmd(self):
        import getpass

        pprompt = lambda: (getpass.getpass('Password: '), getpass.getpass('Retype password: '))
        p1, p2 = pprompt()

        if p1 != p2:
            print 'ERR - Passwords do not match'
            return None

        if (len(p1) < 4 or len(p2) < 4):
            print 'ERR - Password must have a min length of 5 characters'
            return None

        return p2

    def passwd(self):
        from ica.model import User, Session

        if (len(self.args) < 1 or len(self.args) > 2):
            print self.parser.format_help()
            return

        username = self.args[0]
        user = User.by_user_name(unicode(username))

        if len(self.args) == 2:
            passwd = self.args[1]
        else:
            passwd = self.passwd_cmd()

        if passwd is None:
            return

        if user is None:
            print 'ERR - User not found \'%s\'' % username
            return

        print ('Editing user: %s' % user.user_name)
        user.password = passwd
        Session.commit()
        print 'OK - Done'

    def remove_confirm(self, user):
        yes = set(['yes','y', 'ye', ''])
        no = set(['no','n'])

        print ('Confirm remove user \'%s\': (yes/no)' % user)
        choice = raw_input().lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print "Please respond with 'yes' or 'no'"
            return False


    def remove(self, cmd):
        from ica.model import User, Session

        if len(self.args) != 1:
            print self.parser.format_help()
            return

        user = User.by_user_name(unicode(cmd))
        
        if user is None:
            print 'ERR - User not found \'%s\'' % cmd
            return

        if self.remove_confirm(cmd) is False:
            return

        print ('Removing user: %s' % user.user_name)

        Session.delete(user)
        Session.commit()

        print 'OK - Done'