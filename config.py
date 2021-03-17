"""
Application configuration module
"""
import sys
from os.path import join, dirname

from dynaconf.base import Settings
from dynaconf.loaders import settings_loader
from news_service_lib import ConfigProfile

from log_config import get_logger

LOGGER = get_logger()

RESOURCES_PATH = join(dirname(__file__), 'resources')
CONFIGS_PATH = join(dirname(__file__), 'configs')
config = Settings()


def load_config(profile: str):
    """
    Load the configuration for the provided profile

    Args:
        profile: name of the profile to search for the configuration

    """
    try:
        config_profile = ConfigProfile[profile]
    except KeyError:
        LOGGER.error(f'Configuration profile {profile} not found. Exiting...')
        sys.exit(1)

    config_file_path = join(CONFIGS_PATH, config_profile.yml)
    settings_loader(config, filename=config_file_path)
