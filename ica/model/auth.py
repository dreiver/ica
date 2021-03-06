import md5
import sha
from datetime import datetime
from pylons import config

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import String, Unicode, UnicodeText, Integer, DateTime, \
                             Boolean, Float
from sqlalchemy.orm import relation, backref, synonym

from ica.model.meta import Base, metadata, Session


# This is the association table for the many-to-many relationship between
# groups and permissions.
group_permission_table = Table('group_permission', metadata,
    Column('group_id', Integer, ForeignKey('group.group_id', onupdate="CASCADE", ondelete="CASCADE")),
    Column('permission_id', Integer, ForeignKey('permission.permission_id', onupdate="CASCADE", ondelete="CASCADE"))
)

# This is the association table for the many-to-many relationship between
# groups and members - this is, the memberships.
user_group_table = Table('user_group', metadata,
    Column('user_id', Integer, ForeignKey('user.user_id', onupdate="CASCADE", ondelete="CASCADE")),
    Column('group_id', Integer, ForeignKey('group.group_id', onupdate="CASCADE", ondelete="CASCADE"))
)

# auth model

class Group(Base):
    """An ultra-simple group definition.
    """
    __tablename__ = 'group'

    group_id = Column(Integer, autoincrement=True, primary_key=True)

    group_name = Column(Unicode(16), unique=True)

    display_name = Column(Unicode(255))

    created = Column(DateTime, default=datetime.now)

    users = relation('User', secondary=user_group_table, backref='groups')

    #def __repr__(self):
    #    return '<Group: name=%s>' % self.group_name

class User(Base):
    """Reasonably basic User definition. Probably would want additional
    attributes.
    """
    __tablename__ = 'user'

    user_id = Column(Integer, autoincrement=True, primary_key=True)

    user_name = Column(Unicode(16), unique=True)

    email_address = Column(Unicode(255), unique=True)

    display_name = Column(Unicode(255))

    _password = Column('password', Unicode(40))

    created = Column(DateTime, default=datetime.now)

    token = Column(Unicode(20), unique=True)

    theme = Column(Unicode(10))

    extern_uid = Column(Unicode(255), unique=True)

    provider = Column(Unicode(10))

    client_type = Column(Unicode(10))

    location = Column(Unicode(128))

    company = Column(Unicode(128))

    #department = Column(Unicode(200, convert_unicode=False))

    #def __repr__(self):
    #    return '<User: email="%s", display name="%s">' % (
    #            self.email_address, self.display_name)

    @property
    def permissions(self):
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms

    @classmethod
    def by_email_address(cls, email):
        """A class method that can be used to search users
        based on their email addresses since it is unique.
        """
        return Session.query(cls).filter(cls.email_address==email).first()

    @classmethod
    def by_user_name(cls, username):
        return Session.query(cls).filter(cls.user_name==username).first()

    @classmethod
    def by_token(cls, token):
        return Session.query(cls).filter(cls.token==token).first()

    @classmethod
    def by_extern_uid(cls, extern_uid):
        return Session.query(cls).filter(cls.extern_uid==extern_uid).first()

    def _set_password(self, password):
        """encrypts password on the fly using the encryption
        algo defined in the configuration
        """
        #algorithm = config.get('authorize.hashmethod', None)
        algorithm = 'sha1'
        self._password = self.__encrypt_password(algorithm, password)

    def _get_password(self):
        """returns password
        """
        return self._password

    password = synonym('password', descriptor=property(_get_password,
                                                       _set_password))

    def __encrypt_password(self, algorithm, password):
        """Hash the given password with the specified algorithm. Valid values
        for algorithm are 'md5' and 'sha1'. All other algorithm values will
        be essentially a no-op."""
        hashed_password = password

        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')

        else:
            password_8bit = password

        if "md5" == algorithm:
            hashed_password = md5.new(password_8bit).hexdigest()

        elif "sha1" == algorithm:
            hashed_password = sha.new(password_8bit).hexdigest()

        # TODO: re-add the possibility to provide own hasing algo
        # here... just get the real config...

        #elif "custom" == algorithm:
        #    custom_encryption_path = turbogears.config.get(
        #        "identity.custom_encryption", None )
        #
        #    if custom_encryption_path:
        #        custom_encryption = turbogears.util.load_class(
        #            custom_encryption_path)

        #    if custom_encryption:
        #        hashed_password = custom_encryption(password_8bit)

        # make sure the hased password is an UTF-8 object at the end of the
        # process because SQLAlchemy _wants_ a unicode object for Unicode columns
        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')

        return hashed_password

    def validate_password(self, password):
        """Check the password against existing credentials.
        """
        #identity = config.get('identity', None)
        #if identity is None:
        #    return password
        #algorithm = identity.get('password_encryption_method', None)
        algorithm = 'sha1'
        return self.password == self.__encrypt_password(algorithm, password)


class Permission(Base):
    """A relationship that determines what each Group can do
    """
    __tablename__ = 'permission'

    permission_id = Column(Integer, autoincrement=True, primary_key=True)

    permission_name = Column(Unicode(16), unique=True)

    description = Column(Unicode(255))

    groups = relation(Group, secondary=group_permission_table, backref='permissions')
