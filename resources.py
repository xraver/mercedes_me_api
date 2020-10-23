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

class MercedesMeResource:
    def __init__( self, name, version, href, status=None, timestamp=None, valid=False ):
        self.name = name 
        self.version = version
        self.href = href
        self.status = status
        self.timestamp = timestamp
        self.valid = valid

    def getJson(self):
        return ({ 
            "name" : self.name,
            "version" : self.version,
            "href" : self.href,
            "status" : self.status,
            "timestamp" : self.timestamp,
            "valid" : self.valid,
            })

class MercedesMeResourcesDB:

    database = { }
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

        found = False
        resources = None

        if not os.path.isfile(self.config.resources_file):
            # Resources File not present - Retriving new one from server
            logger.error ("Resource File missing - Creating a new one.")
            found = False
        else:
            with open(self.config.resources_file, 'r') as file:
                try:
                    resources = json.load(file)
                    if (not self.CheckResources(resources)):
                        raise ValueError
                    else:
                        found = True
                except ValueError:
                    logger.error ("Error reading resource file - Creating a new one.")
                    found = False

        if ( not found ):
            # Not valid or file missing
            resources = self.RetriveResourcesList()
            if( resources == None ):
                # Not found or wrong
                logger.error ("Error retriving resource list.")
                return False
            else:
                # import and write
                self.ImportResourcesList(resources)
                self.WriteResourcesFile()
                return True
        else:
            # Valid: just import
            self.ImportResourcesList(resources)
            return True

    ########################
    # Check Resources
    ########################
    def CheckResources(self, resources):
        if "reason" in resources:
            logger.error ("Error retriving available resources - " + resources["reason"] + " (" + str(resources["code"]) + ")")
            return False
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
    # Retrive Resources List
    ########################
    def RetriveResourcesList(self):
        resName = "resources"
        resURL = self.config.res_url_prefix + "/vehicles/" + self.config.vin + "/" + resName
        resources = GetResource(resName, resURL, self.config)
        if not self.CheckResources(resources):
            logger.error ("Error retriving available resources")
            return None
        else:
            return resources

    ########################
    # Import Resources List
    ########################
    def ImportResourcesList(self, resources):
        for res in resources:
            if("status" in res):
                self.database[res["name"]] = MercedesMeResource (res["name"], res["version"], res["href"], res["status"], res["timestamp"], res["valid"])
            else:
                self.database[res["name"]] = MercedesMeResource (res["name"], res["version"], res["href"])

    ########################
    # Write Resources File
    ########################
    def WriteResourcesFile(self):
        output = []
        # Extract List
        for res in self.database:
            output.append( self.database[res].getJson() )
        # Write File
        with open(self.config.resources_file, 'w') as file:
            json.dump(output, file)

    ########################
    # Print Available Resources
    ########################
    def PrintAvailableResources(self):
        print ("Found %d resources" % len(self.database) + ":")
        for res in self.database:
            print (self.database[res].name + ": " + self.config.res_url_prefix + self.database[res].href)

    ########################
    # Print Resources Status
    ########################
    def PrintResourcesStatus(self, valid = True):
        for res in self.database:
            if((not valid) | self.database[res].valid):
                print (self.database[res].name + ":")
                print ("\tvalid: " + str(self.database[res].valid))
                print ("\tstatus: " + self.database[res].status)
                print ("\ttimestamp: " + str(self.database[res].timestamp))

    ########################
    # Update Resources Status
    ########################
    def UpdateResourcesStatus(self):
        for res in self.database:
            resName = self.database[res].name
            resURL = self.config.res_url_prefix + self.database[res].href
            result = GetResource(resName, resURL, self.config)
            if not "reason" in result:
                self.database[res].valid = True
                self.database[res].timestamp = result[resName]["timestamp"]
                self.database[res].status = result[resName]["value"]
        # Write Resource File
        self.WriteResourcesFile()
