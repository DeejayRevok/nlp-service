"""
Application configuration module
"""
from os.path import join, dirname

from dynaconf.base import Settings

RESOURCES_PATH = join(dirname(__file__), 'resources')
CONFIGS_PATH = join(dirname(__file__), 'configs')
config = Settings()
