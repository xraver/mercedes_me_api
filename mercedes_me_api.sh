#!/bin/bash

# Author: G. Ravera
# Version 0.5
# Creation Date: 28/09/2020
#
# Change log:
#             28/09/2020 - 0.1 - First Issue
#             18/10/2020 - 0.2 - Added the possibility to retrieve the list of resources available
#             03/12/2020 - 0.3 - Fix in resources list
#             18/12/2020 - 0.4 - Added macOS support (robert@klep.name)
#             19/12/2020 - 0.5 - Added Electric Vehicle Status support
#             23/12/2020 - 0.6 - Added PayAsYouDrive support (danielrheinbay@gmail.com)

# Script Name & Version
NAME="mercedes_me_api.sh"
VERSION="0.6"

# Script Parameters
TOKEN_FILE=".mercedesme_token"
CONFIG_FILE=".mercedesme_config"
# Mercedes me Application Parameters
REDIRECT_URL="https://localhost"
SCOPE="mb:vehicle:mbdata:fuelstatus%20mb:vehicle:mbdata:vehiclestatus%20mb:vehicle:mbdata:vehiclelock%20mb:vehicle:mbdata:evstatus%20mb:vehicle:mbdata:payasyoudrive%20offline_access"
RES_URL_PREFIX="https://api.mercedes-benz.com/vehicledata/v2"
# Resources
RES_FUEL=(rangeliquid tanklevelpercent)
RES_LOCK=(doorlockstatusvehicle doorlockstatusdecklid doorlockstatusgas positionHeading)
RES_STAT=(decklidstatus doorstatusfrontleft doorstatusfrontright doorstatusrearleft doorstatusrearright \
          interiorLightsFront interiorLightsRear lightswitchposition readingLampFrontLeft readingLampFrontRight \
          rooftopstatus sunroofstatus \
          windowstatusfrontleft windowstatusfrontright windowstatusrearleft windowstatusrearright
)
RES_ELECTRIC=(soc rangeelectric)
RES_ODO=(odo)

# set "extended regular expression" argument for sed based on OS
if [ "X$(uname -s)" = "XDarwin" ]
then
  SED_FLAG="-E"
else
  SED_FLAG="-r"
fi

# Credentials
CLIENT_ID=""
CLIENT_SECRET=""
VEHICLE_ID=""
# Loading Credentials
if [[ -f "$CONFIG_FILE" ]]; then
  . $CONFIG_FILE
fi
if [ -z $CLIENT_ID ] | [ -z $CLIENT_ID ] | [ -z $CLIENT_ID ]; then
  echo "Please create $CONFIG_FILE with CLIENT_ID=\"\", CLIENT_SECRET=\"\", VEHICLE_ID=\"\""
  exit
fi

# Formatting RES_URL
RES_URL="$RES_URL_PREFIX/vehicles/$VEHICLE_ID/resources"

function usage ()
{
  echo "Usage:    $NAME <arguments>"
  echo
  echo "Example:  $NAME --token --fuel"
  echo "     or:  $NAME -l"
  echo
  echo "Arguments:"
  echo "    -t, --token           Procedure to obtatin the Access Token (stored into $TOKEN_FILE)"
  echo "    -r, --refresh         Procedure to refresh the Access Token (stored into $TOKEN_FILE)"
  echo "    -f, --fuel            Retrieve the Fuel Status of your Vehicle"
  echo "    -l, --lock            Retrieve the Lock Status of your Vehicle"
  echo "    -s, --status          Retrieve the General Status of your Vehicle"
  echo "    -e, --electric-status Retrieve the General Electric Status of your Vehicle"
  echo "    -o, --odometer        Retrieve the Odometer reading of your Vehicle"
  echo "    -R, --resources       Retrieve the list of available resources of your Vehicle"
  exit
}

function parse_options ()
{
	# Check Options
	OPT=$(getopt -o trflseoR --long token,refresh,fuel,lock,status,electric-status,odometer,resources -n "$NAME parse-error" -- "$@")
	if [ $? != 0 ] || [ $# -eq 0 ]; then
		usage
	fi

	eval set -- "$OPT"

	# Parse Options
	while [ $# -gt 0 ]; do
		case $1 in
			-t | --token )
				getAuthCode
				shift
				;;
			-r | --refresh )
				refreshAuthCode	
				shift
				;;
			-f | --fuel )
				printStatus "${RES_FUEL[@]}"
				shift
				;;
			-l | --lock )
				printStatus "${RES_LOCK[@]}"
				shift
				;;
			-s | --status )
				printStatus "${RES_STAT[@]}"
				shift
				;;
			-e | --electric-status )
				printStatus "${RES_ELECTRIC[@]}"
				shift
				;;
			-o | --odometer )
				printStatus "${RES_ODO[@]}"
				shift
				;;
			-R | --resources )
				printResources
				shift
				;;
			* ) shift ;;
		esac
	done
}

function generateBase64 ()
{
  BASE64=$(echo -n $CLIENT_ID:$CLIENT_SECRET | base64 | sed $SED_FLAG 's/ //')
  BASE64=$(echo $BASE64 | sed $SED_FLAG 's/ //')
}

function getAuthCode () 
{
  generateBase64
  
  echo "Open the browser and insert this link:"
  echo 
  echo "https://id.mercedes-benz.com/as/authorization.oauth2?response_type=code&client_id=$CLIENT_ID&redirect_uri=$REDIRECT_URL&scope=$SCOPE"
  #echo "https://id.mercedes-benz.com/as/authorization.oauth2?response_type=code&client_id=$CLIENT_ID&redirect_uri=$REDIRECT_URL&scope=$SCOPE&state=$STATE"
  echo 
  echo "Copy the code in the url:"

  read AUTH_CODE

  TOKEN=$(curl --request POST \
               --url https://id.mercedes-benz.com/as/token.oauth2 \
               --header "Authorization: Basic $BASE64" \
               --header "content-type: application/x-www-form-urlencoded" \
               --data "grant_type=authorization_code&code=$AUTH_CODE&redirect_uri=$REDIRECT_URL")

  echo $TOKEN > $TOKEN_FILE
}

function refreshAuthCode ()
{
  generateBase64
  extractRefreshToken

  TOKEN=$(curl --request POST \
               --url https://id.mercedes-benz.com/as/token.oauth2 \
               --header "Authorization: Basic $BASE64" \
               --header "content-type: application/x-www-form-urlencoded" \
               --data "grant_type=refresh_token&refresh_token=$REFRESH_CODE")

  echo $TOKEN > $TOKEN_FILE
}

function extractAccessToken ()
{
  ACCESS_TOKEN=$(cat $TOKEN_FILE | grep -Eo '"access_token"[^:]*:[^"]*"[^"]+"' | grep -Eo '"[^"]+"$' | tr -d '"')
}

function extractRefreshToken ()
{
  REFRESH_CODE=$(cat $TOKEN_FILE | grep -Eo '"refresh_token"[^:]*:[^"]*"[^"]+"' | grep -Eo '"[^"]+"$' | tr -d '"')
}

function printStatus ()
{
  extractAccessToken

  for r in "$@"
    do
    echo "Retrieving $r:"
    curl -X GET "$RES_URL/$r" -H "accept: application/json;charset=utf-8" -H "authorization: Bearer $ACCESS_TOKEN"
    echo
  done
}

function printResources ()
{
  extractAccessToken

  curl -X GET "$RES_URL" -H "accept: application/json;charset=utf-8" -H "authorization: Bearer $ACCESS_TOKEN"

}

echo $NAME - $VERSION
echo
parse_options $@
