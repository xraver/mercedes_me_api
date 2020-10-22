"""
Author: G. Ravera
Version 0.1
Creation Date: 22/10/2020

Change log:
            22/10/2020 - 0.1 - First Issue
"""
import argparse
import base64
from configobj import ConfigObj
import getopt
import logging
import json
import os
import requests
import sys

# URLs
oauth_url = "https://id.mercedes-benz.com/as/token.oauth2"
res_url_prefix = "https://api.mercedes-benz.com/vehicledata/v2"
# File Parameters
CONF_CLIENT_ID = "CLIENT_ID"
CONF_CLIENT_SECRET = "CLIENT_SECRET"
CONF_VEHICLE_ID = "VEHICLE_ID"
# Config Parameters
MercedeMeConfig = { 
            "name": "Mercedes Me API",
            "domain": "mercedesmeapi",
            "version": "0.1",
            "token_file": ".mercedesme_token",
            "credentials_file": ".mercedesme_credentials",
            "available_resources_file": ".mercedesme_resources",
            "redirect_uri": "https://localhost",
            "scope": "mb:vehicle:mbdata:fuelstatus%20mb:vehicle:mbdata:vehiclestatus%20mb:vehicle:mbdata:vehiclelock%20offline_access",
            "client_id": "",
            "client_secret": "",
            "vin": "",
            "base64": "",
            "access_token": "",
            "refresh_token": "",
}
# Available Resources (Array)
availableResources = {}
# Response Validity
valid_res = False
# Logger
logger = logging.getLogger(__name__)

########################
# Read Configuration
########################
def ReadCfg():
    global availableResources

    # Read Credentials
    if not os.path.isfile(MercedeMeConfig['credentials_file']):
        logger.error ("Credential File " + MercedeMeConfig['credentials_file'] + " not found")
        return False
    f = ConfigObj(MercedeMeConfig['credentials_file'])
    MercedeMeConfig['client_id'] = f.get(CONF_CLIENT_ID)
    if not MercedeMeConfig['client_id']:
        logger.error ("No "+ CONF_CLIENT_ID + " found in the configuration")
        return False
    MercedeMeConfig['client_secret'] = f.get(CONF_CLIENT_SECRET)
    if not MercedeMeConfig['client_secret']:
        logger.error ("No "+ CONF_CLIENT_SECRET + " found in the configuration")
        return False
    MercedeMeConfig['vin'] = f.get(CONF_VEHICLE_ID)
    if not MercedeMeConfig['vin']:
        logger.error ("No "+ CONF_VEHICLE_ID + " found in the configuration")
        return False
    b64_str = MercedeMeConfig['client_id'] + ":" + MercedeMeConfig['client_secret']
    b64_bytes = base64.b64encode( b64_str.encode('ascii') )
    MercedeMeConfig['base64'] = b64_bytes.decode('ascii')

    # Read Token
    if not os.path.isfile(MercedeMeConfig['token_file']):
        logger.error ("Token File missing - Creating a new one")
        token = CreateToken()
        if token == None:
            logger.error ("Error creating token")
            return False
    else:
        with open(MercedeMeConfig['token_file'], 'r') as file:
            try:
                token = json.load(file)
            except ValueError:
                token = {}
            if not CheckToken(token):
                logger.error ("Token File not correct - Creating a new one")
                token = CreateToken()
                if token == None:
                    return False
    # Save Token
    MercedeMeConfig['access_token'] = token['access_token']
    MercedeMeConfig['refresh_token'] = token['refresh_token']

    # Get Resources List
    if not os.path.isfile(MercedeMeConfig['available_resources_file']):
        logger.error ("Resource File missing - Creating a new one")
        return CreateResourcesFile()
    else:
        with open(MercedeMeConfig['available_resources_file'], 'r') as file:
            try:
                availableResources = json.load(file)
            except ValueError:
                availableResources = {}
            if not CheckResources(availableResources):
                logger.error ("Resource File not correct - Creating a new one")
                return CreateResourcesFile()

    return True

########################
# Write Token
########################
def WriteToken(token):
    with open(MercedeMeConfig['token_file'], 'w') as file:
        json.dump(token, file)

########################
# Check Token
########################
def CheckToken(token):
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
def CreateToken():
    print( "Open the browser and insert this link:\n" )
    print( "https://id.mercedes-benz.com/as/authorization.oauth2?response_type=code&client_id=" + MercedeMeConfig["client_id"] + "&redirect_uri=" + MercedeMeConfig["redirect_uri"] + "&scope=" + MercedeMeConfig["scope"] + "\n")
    print( "Copy the code in the url:")
    auth_code = input()

    headers = {
        "Authorization": "Basic " + MercedeMeConfig['base64'],
        "content-type": "application/x-www-form-urlencoded"
    }
    data = "grant_type=authorization_code&code=" + auth_code + "&redirect_uri=" + MercedeMeConfig["redirect_uri"]

    res = requests.post(oauth_url, data = data, headers = headers)
    try:
        token = res.json()
    except ValueError:
        logger.error ("Error retriving token " + str(res.status_code))
        return None

    # Check Token
    if not CheckToken(token):
        return None
    else:
        WriteToken(token)
        return token

########################
# Refresh Token
########################
def RefreshToken():
    headers = {
        "Authorization": "Basic " + MercedeMeConfig['base64'],
        "content-type": "application/x-www-form-urlencoded"
    }
    data = "grant_type=refresh_token&refresh_token=" + MercedeMeConfig['refresh_token']

    res = requests.post(oauth_url, data = data, headers = headers)
    try:
        token = res.json()
    except ValueError:
        logger.error ("Error refreshing token: " + str(res.status_code))
        return False

    MercedeMeConfig['access_token'] = token['access_token']
    MercedeMeConfig['refresh_token'] = token['refresh_token']

    WriteToken(token)

    return True

########################
# Init Resources
########################
def InitResources():
    # Create Empty Status
    for res in availableResources:
        res["status"] = ""
        res["timestamp"] = 0
        res["valid"] = False

########################
# Write Resources File
########################
def WriteResourcesFile():
    with open(MercedeMeConfig['available_resources_file'], 'w') as file:
        json.dump(availableResources, file)

########################
# Check Resources
########################
def CheckResources(resources):
    if "error" in resources:
        if "error_description" in resources:
            logger.error ("Error retriving resources: " + resources["error_description"])
        else:
            logger.error ("Error retriving resources: " + resources["error"])
        return False
    if len(resources) == 0:
        logger.error ("Empty resources found.")
        return False

    return True

########################
# Create Resources File
########################
def CreateResourcesFile():
    global availableResources
    resName = "resources"
    resURL = res_url_prefix + "/vehicles/" + MercedeMeConfig['vin'] + "/" + resName
    availableResources = GetResource(resName, resURL)
    if valid_res:
        InitResources()
        WriteResourcesFile()
        return True
    else:
        logger.error ("Error retriving available resources")
        logger.error ("-> " + availableResources["reason"] + " (" + str(availableResources["code"]) + ")")
        return False

########################
# GetResource
########################
def GetResource(resourceName, resourceURL):
    global valid_res

    # Set Header
    headers = {
        "accept": "application/json;charset=utf-8", 
        "authorization": "Bearer "+MercedeMeConfig['access_token']
    }

    # Send Request
    res = requests.get(resourceURL, headers=headers)
    try:
        data = res.json()
        valid_res = True
    except ValueError:
        data = { "reason": "No Data",
                 "code" : res.status_code 
        }
        valid_res = False

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
        valid_res = False
    return data

########################
# Print Available Resources
########################
def PrintAvailableResources():
    print ("Found %d resources" % len(availableResources) + ":")
    for res in availableResources:
        print (res["name"] + ": " + res_url_prefix + res["href"])

########################
# Print Resources Status
########################
def PrintResourcesStatus(valid = True):
    for res in availableResources:
        if((not valid) | res["valid"]):
            print (res["name"] + ":")
            print ("\tvalid: " + str(res["valid"]))
            print ("\tstatus: " + res["status"])
            print ("\ttimestamp: " + str(res["timestamp"]))

########################
# Update Resources Status
########################
def UpdateResourcesStatus():
    for res in availableResources:
        resName = res["name"]
        resURL = res_url_prefix + res["href"]
        result = GetResource(resName, resURL)
        if valid_res:
            res["valid"] = True
            res["timestamp"] = result[resName]["timestamp"]
            res["status"] = result[resName]["value"]
    # Write Resource File
    WriteResourcesFile()

########################
# Parse Input
########################
def ParseInput():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', action='store_true', help="Procedure to obtatin the Access Token")
    parser.add_argument('-r', '--refresh', action='store_true', help="Procedure to refresh the Access Token")
    parser.add_argument('-s', '--status', action='store_true', help="Retrive the Status of your Vehicle")
    parser.add_argument('-R', '--resources', action='store_true', help="Retrive the list of available resources of your Vehicle")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + MercedeMeConfig['version'])

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        exit(1)

    return parser.parse_args()

########################
# Main
########################
if __name__ == "__main__":
    args = ParseInput()

    # Reading Configuration
    if not ReadCfg():
        logger.error ("Error reading configuration")
        exit (1)

    if ( args.token == True):
        if not CreateToken():
            logger.error ("Error creating token")
            exit (1)

    if (args.refresh == True):
        if not RefreshToken():
            logger.error ("Error refreshing token")
            exit (1)
            
    if (args.resources):
        PrintAvailableResources()

    if (args.status == True):
        UpdateResourcesStatus()
        PrintResourcesStatus()
