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
from resources import MercedesMeResources

# Logger
logger = logging.getLogger(__name__)

class MercedesMeData:
    def __init__(self):
        # Configuration Data
        self.config = MercedesMeConfig()
        # Resource Data
        self.resources = MercedesMeResources(self.config)

########################
# Parse Input
########################
def ParseInput():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', action='store_true', help="Procedure to obtatin the Access Token")
    parser.add_argument('-r', '--refresh', action='store_true', help="Procedure to refresh the Access Token")
    parser.add_argument('-s', '--status', action='store_true', help="Retrive the Status of your Vehicle")
    parser.add_argument('-R', '--resources', action='store_true', help="Retrive the list of available resources of your Vehicle")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + data.config.version)

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        exit(1)

    return parser.parse_args()

########################
# Main
########################
if __name__ == "__main__":

    # Creating Data Structure
    data = MercedesMeData()

    args = ParseInput()

    # Reading Configuration
    if not data.config.ReadConfig():
        logger.error ("Error initializing configuration")
        exit (1)

    if not data.resources.ReadResources():
        logger.error ("Error initializing resources")
        exit (1)

    if (args.token == True):
        if not data.config.CreateToken():
            logger.error ("Error creating token")
            exit (1)

    if (args.refresh == True):
        if not data.config.RefreshToken():
            logger.error ("Error refreshing token")
            exit (1)
            
    if (args.resources):
        data.resources.PrintAvailableResources()

    if (args.status == True):
        data.resources.UpdateResourcesStatus()
        data.resources.PrintResourcesStatus()
