"""Setup the ica application"""
import logging

from ica.config.environment import load_environment
from ica.model.meta import Base, Session

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup ica here"""
    # Don't reload the app if it was loaded under the testing environment
    load_environment(conf.global_conf, conf.local_conf)

    log.info("Creating tables")
    Base.metadata.drop_all(checkfirst=True, bind=Session.bind)
    Base.metadata.create_all(bind=Session.bind)
    log.info("Successfully setup")