"""
Mercedes Me APIs

Author: G. Ravera

For more details about this component, please refer to the documentation at
https://github.com/xraver/mercedes_me_api/
"""
import logging
import requests

from .const import *

# Logger
_LOGGER = logging.getLogger(__name__)

########################
# GetResource
########################
def GetResource(resourceURL, config):

    # Set Header
    headers = {
        "accept": "application/json;charset=utf-8",
        "authorization": f"Bearer {config.token.access_token}",
    }

    # Send Request
    res = requests.get(resourceURL, headers=headers)
    try:
        data = res.json()
    except ValueError:
        data = {"reason": "No Data", "code": res.status_code}

    # Check Error
    if not res.ok:
        if "reason" in data:
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
                reason = (
                    "The service received too many requests in a given amount of time"
                )
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
def GetToken(tokenURL, headers, data, refresh=True):
    res = requests.post(tokenURL, data=data, headers=headers)
    try:
        data = res.json()
    except ValueError:
        _LOGGER.error(f"Error retrieving token {res.status_code}")
        data = {"reason": "No Data", "code": res.status_code}

    # Check Error
    if not res.ok:
        if "reason" in data:
            reason = data["reason"]
        else:
            if refresh == False:
                # New Token Errors
                if res.status_code == 302:
                    reason = "The request scope is invalid"
                elif res.status_code == 400:
                    reason = "The redirect_uri differs from the registered one"
                elif res.status_code == 401:
                    reason = "The specified client ID is invalid"
                else:
                    reason = "Generic Error"
            else:
                # Refresh Token Errors
                if res.status_code == 400:
                    reason = "The given refresh token is not valid or was already used."
                else:
                    reason = "Generic Error"

        data["reason"] = reason
        data["code"] = res.status_code

    return data
