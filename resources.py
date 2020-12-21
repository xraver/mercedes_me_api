"""
Mercedes Me APIs

Author: G. Ravera

For more details about this component, please refer to the documentation at
https://github.com/xraver/mercedes_me_api/
"""
import json
import logging
import os
from datetime import datetime

from config import MercedesMeConfig
from const import *
from query import *

# Logger
_LOGGER = logging.getLogger(__name__)


class MercedesMeResource:
    def __init__(
        self, name, vin, version, href, state=None, timestamp=None, valid=False
    ):
        self._name = name
        self._version = version
        self._href = href
        self._vin = vin
        self._state = state
        self._timestamp = timestamp
        self._valid = valid
        if timestamp != None:
            self._lastupdate = datetime.fromtimestamp(self._timestamp / 1000)
        else:
            self._lastupdate = 0

    def __str__(self):
        return json.dumps(
            {
                "name": self._name,
                "vin": self._vin,
                "version": self._version,
                "href": self._href,
                "state": self._state,
                "timestamp": self._timestamp,
                "valid": self._valid,
            }
        )

    def getJson(self):
        return {
            "name": self._name,
            "vin": self._vin,
            "version": self._version,
            "href": self._href,
            "state": self._state,
            "timestamp": self._timestamp,
            "valid": self._valid,
        }

    def UpdateState(self, state, timestamp):
        """Update status of the resource."""
        self._state = state
        self._timestamp = timestamp
        self._lastupdate = datetime.fromtimestamp(self._timestamp / 1000)
        self._valid = True

    def unique_id(self):
        """Return the unique id of the sensor."""
        return f"{self._vin}-{self._name}"

    def name(self):
        """Return the name of the sensor."""
        return f"{self._vin}_{self._name}"

    def state(self):
        """Return state for the sensor."""
        return self._state

    def device_state_attributes(self):
        """Return attributes for the sensor."""
        return {
            "valid": self._valid,
            "timestamp": self._timestamp,
            "last_update": self._lastupdate,
        }


class MercedesMeResources:

    ########################
    # Init
    ########################
    def __init__(self, mercedesConfig):

        self.database = []
        self.mercedesConfig = mercedesConfig
        self.resources_file = RESOURCES_FILE

    ########################
    # Read Resources
    ########################
    def ReadResources(self):

        found = False
        resources = None

        if not os.path.isfile(self.resources_file):
            # Resources File not present - Retrieving new one from server
            _LOGGER.error("Resource File missing - Creating a new one.")
            found = False
        else:
            with open(self.resources_file, "r") as file:
                try:
                    resources = json.load(file)
                    if not self.CheckResources(resources):
                        raise ValueError
                    else:
                        found = True
                except ValueError:
                    _LOGGER.error("Error reading resource file - Creating a new one.")
                    found = False

        if not found:
            # Not valid or file missing
            resources = self.RetrieveResourcesList()
            if resources == None:
                # Not found or wrong
                _LOGGER.error("Error retrieving resource list.")
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
            _LOGGER.error(
                f"Error retrieving available resources - {resources['reason']} ({resources['code']})"
            )
            return False
        if "error" in resources:
            if "error_description" in resources:
                _LOGGER.error(
                    f"Error retrieving resources: {resources['error_description']}"
                )
            else:
                _LOGGER.error(f"Error retrieving resources: {resources['error']}")
            return False
        if len(resources) == 0:
            _LOGGER.error("Empty resources found.")
            return False
        return True

    ########################
    # Retrieve Resources List
    ########################
    def RetrieveResourcesList(self):
        resURL = f"{URL_RES_PREFIX}/vehicles/{self.mercedesConfig.vin}/resources"
        resources = GetResource(resURL, self.mercedesConfig)
        if not self.CheckResources(resources):
            _LOGGER.error("Error retrieving available resources")
            return None
        else:
            return resources

    ########################
    # Import Resources List
    ########################
    def ImportResourcesList(self, resources):
        for res in resources:
            if "state" in res:
                self.database.append(
                    MercedesMeResource(
                        res["name"],
                        self.mercedesConfig.vin,
                        res["version"],
                        res["href"],
                        res["state"],
                        res["timestamp"],
                        res["valid"],
                    )
                )
            else:
                self.database.append(
                    MercedesMeResource(
                        res["name"],
                        self.mercedesConfig.vin,
                        res["version"],
                        res["href"],
                    )
                )

    ########################
    # Write Resources File
    ########################
    def WriteResourcesFile(self):
        output = []
        # Extract List
        for res in self.database:
            output.append(res.getJson())
        # Write File
        with open(self.resources_file, "w") as file:
            json.dump(output, file)

    ########################
    # Print Available Resources
    ########################
    def PrintAvailableResources(self):
        print(f"Found {len(self.database)} resources:")
        for res in self.database:
            print(f"{res._name}: {URL_RES_PREFIX}{res._href}")

    ########################
    # Print Resources State
    ########################
    def PrintResourcesState(self, valid=True):
        for res in self.database:
            if (not valid) | res._valid:
                print(f"{res._name}:")
                print(f"\tvalid: {res._valid}")
                print(f"\tstate: {res._state}")
                print(f"\ttimestamp: {res._timestamp}")
                print(f"\tlast_update: {res._lastupdate}")

    ########################
    # Update Resources State
    ########################
    def UpdateResourcesState(self):
        for res in self.database:
            result = GetResource(f"{URL_RES_PREFIX}{res._href}", self.mercedesConfig)
            if not "reason" in result:
                res.UpdateState(
                    result[res._name]["value"], result[res._name]["timestamp"]
                )
        # Write Resource File
        self.WriteResourcesFile()
