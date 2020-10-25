"""
Mercedes Me APIs

Author: G. Ravera

For more details about this component, please refer to the documentation at
https://github.com/xraver/mercedes_me_api/
"""
import base64
import json
import logging
import os
import requests
import voluptuous as vol

from homeassistant.const import (
    CONF_SCAN_INTERVAL,
#    LENGTH_KILOMETERS,
#    LENGTH_MILES,
)

from homeassistant.helpers import discovery, config_validation as cv

from .query import (
	GetResource,
	GetToken
)
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

    token_file = ""
    credentials_file = ""
    resources_file = ""
    client_id = ""
    client_secret = ""
    vin = ""
    scan_interval = ""
    base64 = ""
    access_token = ""
    refresh_token = ""
    token_expires_in = ""
    oauth_url = URL_OAUTH
    res_url_prefix = URL_RES_PREFIX

    ########################
    # Init
    ########################
    def __init__(self, hass, config):
        # Home Assistant structures
        self.hass = hass
        self.config = config
        # Files
        self.token_file = self.hass.config.path(TOKEN_FILE)
        self.resources_file = self.hass.config.path(RESOURCES_FILE)

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
        # Base64
        b64_str = self.client_id + ":" + self.client_secret
        b64_bytes = base64.b64encode( b64_str.encode('ascii') )
        self.base64 = b64_bytes.decode('ascii')

        # Read Token
        if not os.path.isfile(self.token_file):
            _LOGGER.error ("Token File missing - Creating a new one")
            #if (not self.CreateToken()): GRGR -> to be fixed
            if (True):
                _LOGGER.error ("Error creating token")
                return False
        else:
            with open(self.token_file, 'r') as file:
                try:
                    token = json.load(file)
                except ValueError:
                    token = None
                if self.CheckToken(token):
                    # Save Token
                    self.access_token = token['access_token']
                    self.refresh_token = token['refresh_token']
                    self.token_expires_in = token['expires_in']
                    needToRefresh = True
                else:
                    _LOGGER.error ("Token File not correct - Creating a new one")
                    #if (not self.CreateToken()):
                    if (True): # GRGR -> to be fixed
                        _LOGGER.error ("Error creating token")
                        return False

        if (needToRefresh):
            if (not self.RefreshToken()):
                _LOGGER.error ("Error refreshing token")
                return False

        return True

    ########################
    # Write Token
    ########################
    def WriteToken(self, token):
        with open(self.token_file, 'w') as file:
            json.dump(token, file)

    ########################
    # Check Token
    ########################
    def CheckToken(self, token):
        if "error" in token:
            if "error_description" in token:
                _LOGGER.error ("Error retriving token: " + token["error_description"])
            else:
                _LOGGER.error ("Error retriving token: " + token["error"])
            return False
        if len(token) == 0:
            _LOGGER.error ("Empty token found.")
            return False
        if not 'access_token' in token:
            _LOGGER.error ("Access token not present.")
            return False
        if not 'refresh_token' in token:
            _LOGGER.error ("Refresh token not present.")
            return False
        return True

    ########################
    # Create Token
    ########################
    def CreateToken(self):
        print( "Open the browser and insert this link:\n" )
        print( "https://id.mercedes-benz.com/as/authorization.oauth2?response_type=code&client_id=" + self.client_id + "&redirect_uri=" + REDIRECT_URL + "&scope=" + SCOPE + "\n")
        print( "Copy the code in the url:")
        auth_code = input()

        token = GetToken(self, refresh=False, auth_code=auth_code)

        # Check Token
        if not self.CheckToken(token):
            return False
        else:
            # Save Token
            self.WriteToken(token)
            self.access_token = token['access_token']
            self.refresh_token = token['refresh_token']
            self.token_expires_in = token['expires_in']
            return True

    ########################
    # Refresh Token
    ########################
    def RefreshToken(self):

        token = GetToken(self, refresh=True)

        # Check Token
        if not self.CheckToken(token):
            return False
        else:
            # Save Token
            self.WriteToken(token)
            self.access_token = token['access_token']
            self.refresh_token = token['refresh_token']
            self.token_expires_in = token['expires_in']
        return True
