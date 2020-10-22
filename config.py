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

# Logger
logger = logging.getLogger(__name__)

# Software Parameters
NAME = "Mercedes Me API"
DOMAIN = "mercedesmeapi"
VERSION = "0.2"
TOKEN_FILE = ".mercedesme_token"
CREDENTIAL_FILE = ".mercedesme_credentials"
RESOURCES_FILE = ".mercedesme_resources"
REDIRECT_URL = "https://localhost"
SCOPE = "mb:vehicle:mbdata:fuelstatus%20mb:vehicle:mbdata:vehiclestatus%20mb:vehicle:mbdata:vehiclelock%20offline_access"
URL_OAUTH = "https://id.mercedes-benz.com/as/token.oauth2"
URL_RES_PREFIX = "https://api.mercedes-benz.com/vehicledata/v2"

# File Parameters
CONF_CLIENT_ID = "CLIENT_ID"
CONF_CLIENT_SECRET = "CLIENT_SECRET"
CONF_VEHICLE_ID = "VEHICLE_ID"

class MercedesMeConfig:

    name = NAME
    domain = DOMAIN
    version = VERSION
    token_file = TOKEN_FILE
    credentials_file = CREDENTIAL_FILE
    resources_file = RESOURCES_FILE
    redirect_uri = REDIRECT_URL
    scope = SCOPE
    client_id = ""
    client_secret = ""
    vin = ""
    base64 = ""
    access_token = ""
    refresh_token = ""
    oauth_url = URL_OAUTH
    res_url_prefix = URL_RES_PREFIX

    ########################
    # Read Configuration
    ########################
    def ReadConfig(self):
        # Read credentials from file
        if not os.path.isfile(self.credentials_file):
            logger.error ("Credential File " + self.credentials_file + " not found")
            return False
        try:
            f = ConfigObj(self.credentials_file)
        except Exception:
            logger.error ("Wrong "+ self.credentials_file + " file found")
            return False
        # Client ID
        self.client_id = f.get(CONF_CLIENT_ID)
        if not self.client_id:
            logger.error ("No "+ CONF_CLIENT_ID + " found in the configuration")
            return False
        # Client Secret
        self.client_secret = f.get(CONF_CLIENT_SECRET)
        if not self.client_secret:
            logger.error ("No "+ CONF_CLIENT_SECRET + " found in the configuration")
            return False
        # Vehicle ID
        self.vin = f.get(CONF_VEHICLE_ID)
        if not self.vin:
            logger.error ("No "+ CONF_VEHICLE_ID + " found in the configuration")
            return False
        # Base64
        b64_str = self.client_id + ":" + self.client_secret
        b64_bytes = base64.b64encode( b64_str.encode('ascii') )
        self.base64 = b64_bytes.decode('ascii')

        # Read Token
        token_file = self.token_file
        if not os.path.isfile(token_file):
            logger.error ("Token File missing - Creating a new one")
            token = self.CreateToken()
            if token == None:
                logger.error ("Error creating token")
                return False
        else:
            with open(token_file, 'r') as file:
                try:
                    token = json.load(file)
                except ValueError:
                    token = None
                if not self.CheckToken(token):
                    logger.error ("Token File not correct - Creating a new one")
                    token = self.CreateToken()
                    if token == None:
                        logger.error ("Error creating token")
                        return False
        # Save Token
        self.access_token = token['access_token']
        self.refresh_token = token['refresh_token']
        return True

    ########################
    # Write Token
    ########################
    def WriteToken(self, token):
        token_file = self.token_file
        with open(token_file, 'w') as file:
            json.dump(token, file)

    ########################
    # Check Token
    ########################
    def CheckToken(self, token):
        if "error" in token:
            if "error_description" in token:
                logger.error ("Error retriving token: " + token["error_description"])
            else:
                logger.error ("Error retriving token: " + token["error"])
            return False
        if len(token) == 0:
            logger.error ("Empty token found.")
            return False
        if not 'access_token' in token:
            logger.error ("Access token not present.")
            return False
        if not 'refresh_token' in token:
            logger.error ("Refresh token not present.")
            return False
        return True

    ########################
    # Create Token
    ########################
    def CreateToken(self):
        print( "Open the browser and insert this link:\n" )
        print( "https://id.mercedes-benz.com/as/authorization.oauth2?response_type=code&client_id=" + self.client_id + "&redirect_uri=" + self.redirect_uri + "&scope=" + self.scope + "\n")
        print( "Copy the code in the url:")
        auth_code = input()

        token = GetToken(self, refresh=False, auth_code=auth_code)

        # Check Token
        if not self.CheckToken(token):
            return None
        else:
            self.WriteToken(token)
            return token

    ########################
    # Refresh Token
    ########################
    def RefreshToken(self):

        token = GetToken(self, refresh=True)

        # Check Token
        if not self.CheckToken(token):
            return None
        else:
            self.WriteToken(token)
            return token
        return True
