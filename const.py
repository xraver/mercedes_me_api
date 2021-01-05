"""
Mercedes Me APIs

Author: G. Ravera

For more details about this component, please refer to the documentation at
https://github.com/xraver/mercedes_me_api/
"""
# Software Name & Version
NAME = "Mercedes Me API"
DOMAIN = "mercedesmeapi"
VERSION = "0.10"
# Software Parameters
TOKEN_FILE = ".mercedesme_token"
CONFIG_FILE = ".mercedesme_config"
RESOURCES_FILE = ".mercedesme_resources"
# Mercedes me Application Parameters
REDIRECT_URL = "https://localhost"
SCOPE = "mb:vehicle:mbdata:fuelstatus%20mb:vehicle:mbdata:vehiclestatus%20mb:vehicle:mbdata:vehiclelock%20mb:vehicle:mbdata:evstatus%20mb:vehicle:mbdata:payasyoudrive%20offline_access"
URL_RES_PREFIX = "https://api.mercedes-benz.com/vehicledata/v2"

# Configuration File Parameters
CONF_CLIENT_ID = "CLIENT_ID"
CONF_CLIENT_SECRET = "CLIENT_SECRET"
CONF_VEHICLE_ID = "VEHICLE_ID"
CONF_ENABLE_RESOURCES_FILE = "ENABLE_RESOURCES_FILE"
