"""
Mercedes Me APIs

Author: G. Ravera

For more details about this component, please refer to the documentation at
https://github.com/xraver/mercedes_me_api/
"""
from datetime import timedelta
import logging

from .config import MercedesMeConfig
from .resources import MercedesMeResources
from .const import *

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
    # Update State
    ########################
    def UpdateToken(self, event_time):
        _LOGGER.debug ("Start Refresh Token")
        self.mercedesConfig.RefreshToken()
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
    hass.helpers.event.track_time_interval(data.UpdateToken, timedelta(seconds=data.mercedesConfig.token_expires_in))

    return True