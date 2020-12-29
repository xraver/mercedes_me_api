"""
Mercedes Me APIs

Author: G. Ravera

For more details about this component, please refer to the documentation at
https://github.com/xraver/mercedes_me_api/
"""
from datetime import timedelta
import logging
import voluptuous as vol

from homeassistant.const import (
    CONF_SCAN_INTERVAL,
#    LENGTH_KILOMETERS,
#    LENGTH_MILES,
)
from homeassistant.helpers import discovery, config_validation as cv

from .config import MercedesMeConfig
from .oauth import MercedesMeOauth
from .resources import MercedesMeResources
from .const import *

# Config Schema
CONFIG_SCHEMA = vol.Schema (
    {
        DOMAIN: vol.Schema (
            {
                vol.Required(CONF_CLIENT_ID): cv.string,
                vol.Required(CONF_CLIENT_SECRET): cv.string,
                vol.Required(CONF_VEHICLE_ID): cv.string,
                vol.Optional(CONF_ENABLE_RESOURCES_FILE, default=False): cv.boolean,
                vol.Optional(CONF_SCAN_INTERVAL, default=30): vol.All(
                    cv.positive_int, vol.Clamp(min=120)
                ),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

# Logger
_LOGGER = logging.getLogger(__name__)

class MercedesMeData:

    ########################
    # Init
    ########################
    def __init__(self, hass, config):
        # Configuration Data
        self.mercedesConfig = MercedesMeConfig(hass, config)
        # Resource Data
        self.mercedesResources = MercedesMeResources(self.mercedesConfig)

    ########################
    # Update State
    ########################
    def UpdateState(self, event_time):
        _LOGGER.debug ("Start Update Resources")
        self.mercedesResources.UpdateResourcesState()
        #hass.helpers.dispatcher.dispatcher_send(UPDATE_SIGNAL)
        _LOGGER.debug ("End Update")

    ########################
    # Update Token
    ########################
    def UpdateToken(self, event_time):
        _LOGGER.debug ("Start Refresh Token")
        self.mercedesConfig.token.RefreshToken()
        #hass.helpers.dispatcher.dispatcher_send(UPDATE_SIGNAL)
        _LOGGER.debug ("End Refresh Token")

########################
# Setup
########################
#async def async_setup(hass, config):
def setup(hass, config):

    # Creating Data Structure
    data = MercedesMeData(hass, config)
    hass.data[DOMAIN] = data

    # Reading Configuration
    if not data.mercedesConfig.ReadConfig():
        _LOGGER.error ("Error initializing configuration")
        return False

    if not data.mercedesResources.ReadResources():
        _LOGGER.error ("Error initializing resources")
        return False

    # Create Task to initializate Platform Sensor
    hass.async_create_task(
        hass.helpers.discovery.async_load_platform("sensor", DOMAIN, {}, config)
    )

    # Create Task to Update Status
    hass.helpers.event.track_time_interval(data.UpdateState, timedelta(seconds=data.mercedesConfig.scan_interval))

    # Create Task to Update Token
    hass.helpers.event.track_time_interval(data.UpdateToken, timedelta(seconds=data.mercedesConfig.token.token_expires_in))

    return True