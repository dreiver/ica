"""The application's model objects"""
from ica.model.meta import Session, Base

from ica.model.auth import (
    User,
    Group,
    Permission,
)

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)
