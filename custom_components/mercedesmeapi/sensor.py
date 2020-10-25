"""
Mercedes Me APIs

Author: G. Ravera

For more details about this component, please refer to the documentation at
https://github.com/xraver/mercedes_me_api/
"""
import logging

from .config import MercedesMeConfig
from .config import DOMAIN
from .resources import MercedesMeResources

#DEPENDENCIES = ['mercedesmeapi']

# Logger
_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, _discovery_info=None):
    """Setup sensor platform."""

    mercedesConfig = hass.data[DOMAIN].mercedesConfig
    mercedesRes = hass.data[DOMAIN].mercedesResources

    async_add_entities(mercedesRes.database, True)
