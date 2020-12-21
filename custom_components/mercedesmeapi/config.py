"""
Mercedes Me APIs

Author: G. Ravera

For more details about this component, please refer to the documentation at
https://github.com/xraver/mercedes_me_api/
"""
import logging
import voluptuous as vol

from homeassistant.const import (
    CONF_SCAN_INTERVAL,
#    LENGTH_KILOMETERS,
#    LENGTH_MILES,
)

from homeassistant.helpers import discovery, config_validation as cv

from .oauth import MercedesMeOauth
from .const import *

# Logger
_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema (
    {
        DOMAIN: vol.Schema (
            {
                vol.Required(CONF_CLIENT_ID): cv.string,
                vol.Required(CONF_CLIENT_SECRET): cv.string,
                vol.Required(CONF_VEHICLE_ID): cv.string,
                vol.Optional(CONF_SCAN_INTERVAL, default=30): vol.All(
                    cv.positive_int, vol.Clamp(min=60)
                ),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

class MercedesMeConfig:

    ########################
    # Init
    ########################
    def __init__(self, hass, config):
        # Home Assistant structures
        self.hass = hass
        self.config = config
        self.client_id = ""
        self.client_secret = ""
        self.vin = ""
        self.token = ""

    ########################
    # Read Configuration
    ########################
    def ReadConfig(self):
        needToRefresh = False

        config = self.config[DOMAIN]
        # Client ID
        self.client_id = config[CONF_CLIENT_ID]
        # Client Secret
        self.client_secret = config[CONF_CLIENT_SECRET]
        # Vehicle ID
        self.vin = config[CONF_VEHICLE_ID]
        # Scan Interval
        self.scan_interval = config[CONF_SCAN_INTERVAL]
        # Read Token
        self.token = MercedesMeOauth(self.hass, self.client_id, self.client_secret)
        if not self.token.ReadToken():
            return False

        return True
