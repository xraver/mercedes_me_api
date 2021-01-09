"""
Mercedes Me APIs

Author: G. Ravera

For more details about this component, please refer to the documentation at
https://github.com/xraver/mercedes_me_api/
"""
import logging
import os

from configobj import ConfigObj

from const import *
from oauth import MercedesMeOauth

# Logger
_LOGGER = logging.getLogger(__name__)


class MercedesMeConfig:

    ########################
    # Init
    ########################
    def __init__(self):
        self.config_file = CONFIG_FILE

    ########################
    # Read Configuration
    ########################
    def ReadConfig(self):
        # Read Config from file
        if not os.path.isfile(self.config_file):
            _LOGGER.error(f"Credential File {self.config_file} not found")
            return False
        try:
            f = ConfigObj(self.config_file)
        except Exception:
            _LOGGER.error(f"Wrong {self.config_file} file found")
            return False
        # Client ID
        self.client_id = f.get(CONF_CLIENT_ID)
        if not self.client_id:
            _LOGGER.error(f"No {CONF_CLIENT_ID} found in the configuration")
            return False
        # Client Secret
        self.client_secret = f.get(CONF_CLIENT_SECRET)
        if not self.client_secret:
            _LOGGER.error(f"No {CONF_CLIENT_SECRET} found in the configuration")
            return False
        # Vehicle ID
        self.vin = f.get(CONF_VEHICLE_ID)
        if not self.vin:
            _LOGGER.error(f"No {CONF_VEHICLE_ID} found in the configuration")
            return False
        # Enable Resources File (optional)
        valueFromFile = f.get(CONF_ENABLE_RESOURCES_FILE)
        if (valueFromFile == "true") | (valueFromFile == "True"):
            self.enable_resources_file = True
        else:
            self.enable_resources_file = False
        # Read Token
        self.token = MercedesMeOauth(self.client_id, self.client_secret)
        if not self.token.ReadToken():
            return False

        return True
