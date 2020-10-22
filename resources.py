"""
Mercedes Me APIs

Author: G. Ravera

For more details about this component, please refer to the documentation at
https://github.com/xraver/mercedes_me_api/
"""
import logging
import json
import os

from config import MercedesMeConfig
from query import GetResource

# Logger
logger = logging.getLogger(__name__)

class MercedesMeResources:

    resources = None
    config = None

    ########################
    # Init
    ########################
    def __init__(self, config):
        self.config = config
        
    ########################
    # Read Resources
    ########################
    def ReadResources(self):
        # Get Resources List
        if not os.path.isfile(self.config.resources_file):
            logger.error ("Resource File missing - Creating a new one.")
            if (self.CreateResourcesFile() == False):
                logger.error ("Error creating resources file.")
                return None
        else:
            with open(self.config.resources_file, 'r') as file:
                try:
                    self.resources = json.load(file)
                except ValueError:
                    resources = None
                if not self.CheckResources():
                    logger.error ("Resource File not correct - Creating a new one.")
                    if (self.CreateResourcesFile() == False):
                        logger.error ("Error creating resources file.")
                        return None
        return True

    ########################
    # Init Resources
    ########################
    def InitResources(self):
        # Create Empty Status
        for res in self.resources:
            res["status"] = ""
            res["timestamp"] = 0
            res["valid"] = False

    ########################
    # Write Resources File
    ########################
    def WriteResourcesFile(self):
        with open(self.config.resources_file, 'w') as file:
            json.dump(self.resources, file)

    ########################
    # Check Resources
    ########################
    def CheckResources(self):
        if "error" in self.resources:
            if "error_description" in self.resources:
                logger.error ("Error retriving resources: " + self.resources["error_description"])
            else:
                logger.error ("Error retriving resources: " + self.resources["error"])
            return False
        if len(self.resources) == 0:
            logger.error ("Empty resources found.")
            return False
        return True

    ########################
    # Create Resources File
    ########################
    def CreateResourcesFile(self):
        resName = "resources"
        resURL = self.config.res_url_prefix + "/vehicles/" + self.config.vin + "/" + resName
        self.resources = GetResource(resName, resURL, self.config)
        if "reason" in self.resources:
            logger.error ("Error retriving available resources - " + self.resources["reason"] + " (" + str(self.resources["code"]) + ")")
            return False
        else:
            self.InitResources()
            self.WriteResourcesFile()
            return True

    ########################
    # Print Available Resources
    ########################
    def PrintAvailableResources(self):
        print ("Found %d resources" % len(self.resources) + ":")
        for res in self.resources:
            print (res["name"] + ": " + self.config.res_url_prefix + res["href"])

    ########################
    # Print Resources Status
    ########################
    def PrintResourcesStatus(self, valid = True):
        for res in self.resources:
            if((not valid) | res["valid"]):
                print (res["name"] + ":")
                print ("\tvalid: " + str(res["valid"]))
                print ("\tstatus: " + res["status"])
                print ("\ttimestamp: " + str(res["timestamp"]))

    ########################
    # Update Resources Status
    ########################
    def UpdateResourcesStatus(self):
        for res in self.resources:
            resName = res["name"]
            resURL = self.config.res_url_prefix + res["href"]
            result = GetResource(resName, resURL, self.config)
            if not "reason" in result:
                res["valid"] = True
                res["timestamp"] = result[resName]["timestamp"]
                res["status"] = result[resName]["value"]
        # Write Resource File
        self.WriteResourcesFile()