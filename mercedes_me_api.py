"""
Mercedes Me APIs

Author: G. Ravera

For more details about this component, please refer to the documentation at
https://github.com/xraver/mercedes_me_api/
"""
import argparse
import logging
import sys

from config import MercedesMeConfig
from const import *
from resources import MercedesMeResources

# Logger
_LOGGER = logging.getLogger(__name__)


class MercedesMeData:
    def __init__(self):
        # Configuration Data
        self.mercedesConfig = MercedesMeConfig()
        # Resource Data
        self.mercedesResources = MercedesMeResources(self.mercedesConfig)


########################
# Parse Input
########################
def ParseInput():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--token",
        action="store_true",
        help="Procedure to obtatin the Access Token",
    )
    parser.add_argument(
        "-r",
        "--refresh",
        action="store_true",
        help="Procedure to refresh the Access Token",
    )
    parser.add_argument(
        "-s",
        "--status",
        action="store_true",
        help="Retrieve the Status of your Vehicle",
    )
    parser.add_argument(
        "-R",
        "--resources",
        action="store_true",
        help="Retrieve the list of available resources of your Vehicle",
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + VERSION
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        exit(1)

    return parser.parse_args()


########################
# Main
########################
if __name__ == "__main__":

    # Reading Arguments
    args = ParseInput()

    # Creating Data Structure
    data = MercedesMeData()

    # Reading Configuration
    if not data.mercedesConfig.ReadConfig():
        _LOGGER.error("Error initializing configuration")
        exit(1)

    # Create Token
    if args.token == True:
        if not data.mercedesConfig.token.CreateToken():
            _LOGGER.error("Error creating token")
            exit(1)

    # Refresh Token
    if args.refresh == True:
        if not data.mercedesConfig.token.RefreshToken():
            _LOGGER.error("Error refreshing token")
            exit(1)

    # Read Resources
    if (args.resources == True) | (args.status == True):
        if not data.mercedesResources.ReadResources():
            _LOGGER.error("Error initializing resources")
            exit(1)

    # Print Available Resources
    if args.resources == True:
        data.mercedesResources.PrintAvailableResources()

    # Print Resources State
    if args.status == True:
        data.mercedesResources.UpdateResourcesState()
        data.mercedesResources.PrintResourcesState()
