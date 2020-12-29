"""
Mercedes Me APIs

Author: G. Ravera

For more details about this component, please refer to the documentation at
https://github.com/xraver/mercedes_me_api/
"""
import logging

from homeassistant.const import (
    CONF_SCAN_INTERVAL,
#    LENGTH_KILOMETERS,
#    LENGTH_MILES,
)

from .const import *
from .oauth import MercedesMeOauth

# Logger
_LOGGER = logging.getLogger(__name__)


class MercedesMeConfig:

    ########################
    # Init
    ########################
    def __init__(self, hass, config):
        # Home Assistant structures
        self.hass = hass
        self.config = config[DOMAIN]

    ########################
    # Read Configuration
    ########################
    def ReadConfig(self):
        # Client ID
        self.client_id = self.config.get(CONF_CLIENT_ID)
        # Client Secret
        self.client_secret = self.config.get(CONF_CLIENT_SECRET)
        # Vehicle ID
        self.vin = self.config.get(CONF_VEHICLE_ID)
        # Enable Resources File (optional)
        self.enable_resources_file = self.config.get(CONF_ENABLE_RESOURCES_FILE)
        # Scan Interval (optional)
        self.scan_interval = self.config.get(CONF_SCAN_INTERVAL)
        # Read Token
        self.token = MercedesMeOauth(self.hass, self.client_id, self.client_secret)
        if not self.token.ReadToken():
            return False

        return True
