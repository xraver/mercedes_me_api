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
from const import *

# Logger
_LOGGER = logging.getLogger(__name__)

class MercedesMeResource:
    def __init__( self, name, vin, version, href, state=None, timestamp=None, valid=False ):
        self._name = name
        self._version = version
        self._href = href
        self._vin = vin
        self._state = state
        self._timestamp = timestamp
        self._valid = valid

    def __str__(self):
        return json.dumps({ 
            "name" : self._name,
            "vin" : self._vin,
            "version" : self._version,
            "href" : self._href,
            "state" : self._state,
            "timestamp" : self._timestamp,
            "valid" : self._valid,
            })

    def getJson(self):
        return ({ 
            "name" : self._name,
            "vin" : self._vin,
            "version" : self._version,
            "href" : self._href,
            "state" : self._state,
            "timestamp" : self._timestamp,
            "valid" : self._valid,
            })

    def name(self):
        """Return the name of the sensor."""
        return self._vin + "_" + self._name

    def state(self):
        """Return state for the sensor."""
        return self._state

    def device_state_attributes(self):
        """Return attributes for the sensor."""
        return ({
                "valid": self._valid,
                "timestamp": self._timestamp,
                })

    def update(self):
        """Fetch new state data for the sensor."""
        resName = self._name
        resURL = URL_RES_PREFIX + self._href
        result = GetResource(resName, resURL, self._config)
        if not "reason" in result:
            self._valid = True
            self._timestamp = result[resName]["timestamp"]
            self._state = result[resName]["value"]

class MercedesMeResources:

    ########################
    # Init
    ########################
    def __init__(self, mercedesConfig):

        self.database = []
        self.mercedesConfig = mercedesConfig

    ########################
    # Read Resources
    ########################
    def ReadResources(self):

        found = False
        resources = None

        if not os.path.isfile(self.mercedesConfig.resources_file):
            # Resources File not present - Retriving new one from server
            _LOGGER.error ("Resource File missing - Creating a new one.")
            found = False
        else:
            with open(self.mercedesConfig.resources_file, 'r') as file:
                try:
                    resources = json.load(file)
                    if (not self.CheckResources(resources)):
                        raise ValueError
                    else:
                        found = True
                except ValueError:
                    _LOGGER.error ("Error reading resource file - Creating a new one.")
                    found = False

        if ( not found ):
            # Not valid or file missing
            resources = self.RetriveResourcesList()
            if( resources == None ):
                # Not found or wrong
                _LOGGER.error ("Error retriving resource list.")
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
            _LOGGER.error ("Error retriving available resources - " + resources["reason"] + " (" + str(resources["code"]) + ")")
            return False
        if "error" in resources:
            if "error_description" in resources:
                _LOGGER.error ("Error retriving resources: " + resources["error_description"])
            else:
                _LOGGER.error ("Error retriving resources: " + resources["error"])
            return False
        if len(resources) == 0:
            _LOGGER.error ("Empty resources found.")
            return False
        return True

    ########################
    # Retrive Resources List
    ########################
    def RetriveResourcesList(self):
        resName = "resources"
        resURL = URL_RES_PREFIX + "/vehicles/" + self.mercedesConfig.vin + "/" + resName
        resources = GetResource(resName, resURL, self.mercedesConfig)
        if not self.CheckResources(resources):
            _LOGGER.error ("Error retriving available resources")
            return None
        else:
            return resources

    ########################
    # Import Resources List
    ########################
    def ImportResourcesList(self, resources):
        for res in resources:
            if("state" in res):
                self.database.append( MercedesMeResource (res["name"], self.mercedesConfig.vin, res["version"], res["href"], res["state"], res["timestamp"], res["valid"]) )
            else:
                self.database.append( MercedesMeResource (res["name"], self.mercedesConfig.vin, res["version"], res["href"]) )

    ########################
    # Write Resources File
    ########################
    def WriteResourcesFile(self):
        output = []
        # Extract List
        for res in self.database:
            output.append( res.getJson() )
        # Write File
        with open(self.mercedesConfig.resources_file, 'w') as file:
            json.dump(output, file)

    ########################
    # Print Available Resources
    ########################
    def PrintAvailableResources(self):
        print ("Found %d resources" % len(self.database) + ":")
        for res in self.database:
            print (res._name + ": " + URL_RES_PREFIX + res._href)

    ########################
    # Print Resources State
    ########################
    def PrintResourcesState(self, valid = True):
        for res in self.database:
            if((not valid) | res._valid):
                print (res._name + ":")
                print ("\tvalid: " + str(res._valid))
                print ("\tstate: " + res._state)
                print ("\ttimestamp: " + str(res._timestamp))

    ########################
    # Update Resources State
    ########################
    def UpdateResourcesState(self):
        _LOGGER.error("Update Resources")
        for res in self.database:
            resName = res._name
            resURL = URL_RES_PREFIX + res._href
            result = GetResource(resName, resURL, self.mercedesConfig)
            if not "reason" in result:
                res._valid = True
                res._timestamp = result[resName]["timestamp"]
                res._state = result[resName]["value"]
        # Write Resource File
        self.WriteResourcesFile()
