"""
Mercedes Me APIs

Author: G. Ravera

For more details about this component, please refer to the documentation at
https://github.com/xraver/mercedes_me_api/
"""
# Software Parameters
NAME = "Mercedes Me API"
DOMAIN = "mercedesmeapi"
VERSION = "0.4"
TOKEN_FILE = ".mercedesme_token"
CREDENTIAL_FILE = ".mercedesme_credentials"
RESOURCES_FILE = ".mercedesme_resources"
REDIRECT_URL = "https://localhost"
SCOPE = "mb:vehicle:mbdata:fuelstatus%20mb:vehicle:mbdata:vehiclestatus%20mb:vehicle:mbdata:vehiclelock%20offline_access"
URL_RES_PREFIX = "https://api.mercedes-benz.com/vehicledata/v2"

# File Parameters
CONF_CLIENT_ID = "CLIENT_ID"
CONF_CLIENT_SECRET = "CLIENT_SECRET"
CONF_VEHICLE_ID = "VEHICLE_ID"
