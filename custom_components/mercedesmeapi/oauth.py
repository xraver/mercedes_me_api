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

from .const import *
from .query import *

URL_OAUTH_BASE = "https://id.mercedes-benz.com/as"
URL_OAUTH_AUTH = f"{URL_OAUTH_BASE}/authorization.oauth2?response_type=code"
URL_OAUTH_TOKEN = f"{URL_OAUTH_BASE}/token.oauth2"

# Logger
_LOGGER = logging.getLogger(__name__)


class MercedesMeOauth:

    ########################
    # Init
    ########################
    def __init__(self, hass, client_id, client_secret):
        # Access Token
        self.access_token = ""
        # Refresh Token
        self.refresh_token = ""
        # Expiration Time
        self.token_expires_in = ""
        # Client ID
        self.client_id = client_id
        # Client Secret
        self.client_secret = client_secret
        # Token File
        self.token_file = hass.config.path(TOKEN_FILE)
        # Base64
        b64_str = f"{client_id}:{client_secret}"
        b64_bytes = base64.b64encode( b64_str.encode('ascii') )
        self.base64 = b64_bytes.decode('ascii')
        # Headers
        self.headers = {
            "Authorization": f"Basic {self.base64}",
            "content-type": "application/x-www-form-urlencoded"
        }

    ########################
    # Read Token
    ########################
    def ReadToken(self):

        found = False
        needToRefresh = False

        # Read Token
        if not os.path.isfile(self.token_file):
            # Token File not present - Creating new one
            _LOGGER.error("Token File missing - Creating a new one")
            found = False
        else:
            with open(self.token_file, "r") as file:
                try:
                    token = json.load(file)
                    if not self.CheckToken(token):
                        raise ValueError
                    else:
                        found = True
                except ValueError:
                    _LOGGER.error("Error reading token file - Creating a new one")
                    found = False

        if not found:
            # Not valid or file missing
            #if (not self.CreateToken()): GRGR -> to be fixed
            if (True):
                _LOGGER.error("Error creating token")
                return False
        else:
            # Valid: just import
            self.access_token = token["access_token"]
            self.refresh_token = token["refresh_token"]
            self.token_expires_in = token["expires_in"]
            needToRefresh = True

        if needToRefresh:
            if not self.RefreshToken():
                _LOGGER.error("Error refreshing token")
                return False

        return True

    ########################
    # Write Token
    ########################
    def WriteToken(self, token):
        with open(self.token_file, "w") as file:
            json.dump(token, file)

    ########################
    # Check Token
    ########################
    def CheckToken(self, token):
        if "reason" in token:
            _LOGGER.error(
                f"Error retrieving token - {token['reason']} ({token['code']})"
            )
            return False
        if "error" in token:
            if "error_description" in token:
                _LOGGER.error(f"Error retrieving token: {token['error_description']}")
            else:
                _LOGGER.error(f"Error retrieving token: {token['error']}")
            return False
        if len(token) == 0:
            _LOGGER.error("Empty token found.")
            return False
        if not "access_token" in token:
            _LOGGER.error("Access token not present.")
            return False
        if not "refresh_token" in token:
            _LOGGER.error("Refresh token not present.")
            return False
        return True

    ########################
    # Create Token
    ########################
    def CreateToken(self):

        auth_url = (
            f"{URL_OAUTH_AUTH}&"
            + f"client_id={self.client_id}&"
            + f"redirect_uri={REDIRECT_URL}&"
            + f"scope={SCOPE}"
        )

        print("Open the browser and insert this link:\n")
        print(f"{auth_url}\n")
        print("Copy the code in the url:")
        auth_code = input()

        data = f"grant_type=authorization_code&code={auth_code}&redirect_uri={REDIRECT_URL}"
        token = GetToken(URL_OAUTH_TOKEN, self.headers, data, refresh=False)

        # Check Token
        if not self.CheckToken(token):
            return False
        else:
            # Save Token
            self.WriteToken(token)
            self.access_token = token["access_token"]
            self.refresh_token = token["refresh_token"]
            self.token_expires_in = token["expires_in"]
            return True

    ########################
    # Refresh Token
    ########################
    def RefreshToken(self):

        data = f"grant_type=refresh_token&refresh_token={self.refresh_token}"
        token = GetToken(URL_OAUTH_TOKEN, self.headers, data, refresh=True)

        # Check Token
        if not self.CheckToken(token):
            return False
        else:
            # Save Token
            self.WriteToken(token)
            self.access_token = token["access_token"]
            self.refresh_token = token["refresh_token"]
            self.token_expires_in = token["expires_in"]
        return True
