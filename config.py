"""
Mercedes Me APIs

Author: G. Ravera

For more details about this component, please refer to the documentation at
https://github.com/xraver/mercedes_me_api/
"""
from configobj import ConfigObj
import base64
import json
import logging
import os
import requests

from query import (
	GetResource,
	GetToken
)
from const import *

# Logger
_LOGGER = logging.getLogger(__name__)

class MercedesMeConfig:

    token_file = ""
    credentials_file = ""
    resources_file = ""
    client_id = ""
    client_secret = ""
    vin = ""
    base64 = ""
    access_token = ""
    refresh_token = ""
    token_expires_in = ""
    oauth_url = URL_OAUTH
    res_url_prefix = URL_RES_PREFIX

    ########################
    # Init
    ########################
    def __init__(self):
        # Files
        self.token_file = TOKEN_FILE
        self.credentials_file = CREDENTIAL_FILE
        self.resources_file = RESOURCES_FILE

    ########################
    # Read Configuration
    ########################
    def ReadConfig(self):
        needToRefresh = False

        # Read credentials from file
        if not os.path.isfile(self.credentials_file):
            _LOGGER.error ("Credential File " + self.credentials_file + " not found")
            return False
        try:
            f = ConfigObj(self.credentials_file)
        except Exception:
            _LOGGER.error ("Wrong "+ self.credentials_file + " file found")
            return False
        # Client ID
        self.client_id = f.get(CONF_CLIENT_ID)
        if not self.client_id:
            _LOGGER.error ("No "+ CONF_CLIENT_ID + " found in the configuration")
            return False
        # Client Secret
        self.client_secret = f.get(CONF_CLIENT_SECRET)
        if not self.client_secret:
            _LOGGER.error ("No "+ CONF_CLIENT_SECRET + " found in the configuration")
            return False
        # Vehicle ID
        self.vin = f.get(CONF_VEHICLE_ID)
        if not self.vin:
            _LOGGER.error ("No "+ CONF_VEHICLE_ID + " found in the configuration")
            return False
        # Base64
        b64_str = self.client_id + ":" + self.client_secret
        b64_bytes = base64.b64encode( b64_str.encode('ascii') )
        self.base64 = b64_bytes.decode('ascii')

        # Read Token
        if not os.path.isfile(self.token_file):
            _LOGGER.error ("Token File missing - Creating a new one")
            if (not self.CreateToken()):
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
                    if (not self.CreateToken()):
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
