"""
Mercedes Me APIs

Author: G. Ravera

For more details about this component, please refer to the documentation at
https://github.com/xraver/mercedes_me_api/
"""
from configobj import ConfigObj
import logging
import os

from oauth import MercedesMeOauth
from const import *

# Logger
_LOGGER = logging.getLogger(__name__)

class MercedesMeConfig:

    ########################
    # Init
    ########################
    def __init__(self):
        self.credentials_file = CREDENTIAL_FILE
        self.client_id = ""
        self.client_secret = ""
        self.vin = ""
        self.token = ""

    ########################
    # Read Configuration
    ########################
    def ReadConfig(self):
        needToRefresh = False

        # Read Credentials from file
        if not os.path.isfile(self.credentials_file):
            _LOGGER.error (f"Credential File {self.credentials_file} not found")
            return False
        try:
            f = ConfigObj(self.credentials_file)
        except Exception:
            _LOGGER.error (f"Wrong {self.credentials_file} file found")
            return False
        # Client ID
        self.client_id = f.get(CONF_CLIENT_ID)
        if not self.client_id:
            _LOGGER.error ("No {CONF_CLIENT_ID} found in the configuration")
            return False
        # Client Secret
        self.client_secret = f.get(CONF_CLIENT_SECRET)
        if not self.client_secret:
            _LOGGER.error ("No {CONF_CLIENT_SECRET} found in the configuration")
            return False
        # Vehicle ID
        self.vin = f.get(CONF_VEHICLE_ID)
        if not self.vin:
            _LOGGER.error ("No {CONF_VEHICLE_ID} found in the configuration")
            return False
        # Read Token
        self.token = MercedesMeOauth(self.client_id, self.client_secret)
        if not self.token.ReadToken():
            return False
        
        return True
