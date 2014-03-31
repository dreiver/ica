"""Pylons environment configuration"""
import os

from jinja2 import Environment, FileSystemLoader
from pylons.configuration import PylonsConfig
from sqlalchemy import engine_from_config

import ica.lib.app_globals as app_globals
import ica.lib.helpers
from ica.config.routing import make_map
from ica.model import init_model

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    config = PylonsConfig()
    
    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='ica', paths=paths)

    config['routes.map'] = make_map(config)
    config['pylons.app_globals'] = app_globals.Globals(config)
    config['pylons.h'] = ica.lib.helpers
    
    # Setup cache object as early as possible
    import pylons
    pylons.cache._push_object(config['pylons.app_globals'].cache)
    
    # Create the Jinja2 Environment
    jinja2_env = Environment(loader=FileSystemLoader(paths['templates']))
    config['pylons.app_globals'].jinja2_env = jinja2_env

    #config['pylons.strict_tmpl_context'] = True

    # Setup the SQLAlchemy database engine
    engine = engine_from_config(config, 'sqlalchemy.')
    init_model(engine)

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)
    
    return config
