"""
Mercedes Me APIs

Author: G. Ravera

For more details about this component, please refer to the documentation at
https://github.com/xraver/mercedes_me_api/
"""
import logging
import requests

from const import *

# Logger
_LOGGER = logging.getLogger(__name__)

########################
# GetResource
########################
def GetResource(resourceName, resourceURL, config):

    # Set Header
    headers = {
        "accept": "application/json;charset=utf-8", 
        "authorization": "Bearer "+ config.access_token
    }

    # Send Request
    res = requests.get(resourceURL, headers=headers)
    try:
        data = res.json()
    except ValueError:
        data = { "reason": "No Data",
                 "code" : res.status_code 
        }

    # Check Error
    if not res.ok:
        if ("reason" in data):
            reason = data["reason"]
        else:
            if res.status_code == 400:
                reason = "Bad Request"
            elif res.status_code == 401:
                reason = "Invalid or missing authorization in header"
            elif res.status_code == 402:
                reason = "Payment required"
            elif res.status_code == 403:
                reason = "Forbidden"
            elif res.status_code == 404:
                reason = "Page not found"
            elif res.status_code == 429:
                reason = "The service received too many requests in a given amount of time"
            elif res.status_code == 500:
                reason = "An error occurred on the server side"
            elif res.status_code == 503:
                reason = "The server is unable to service the request due to a temporary unavailability condition"
            else:
                reason = "Generic Error"
        data["reason"] = reason
        data["code"] = res.status_code
    return data

########################
# GetToken
########################
def GetToken(config, refresh=True, auth_code=""):
    headers = {
        "Authorization": "Basic " + config.base64,
        "content-type": "application/x-www-form-urlencoded"
    }

    if (not refresh):
        # New Token
        data = "grant_type=authorization_code&code=" + auth_code + "&redirect_uri=" + REDIRECT_URL
    else:
        # Refresh
        data = "grant_type=refresh_token&refresh_token=" + config.refresh_token

    res = requests.post(URL_OAUTH, data = data, headers = headers)
    try:
        token = res.json()
    except ValueError:
        _LOGGER.error ("Error retriving token " + str(res.status_code))
        return None

    return token
