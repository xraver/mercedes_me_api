#!/bin/bash

# Author: G. Ravera
# Version 0.2
# Creation Date: 28/09/2020
#
# Change log:
#             28/09/2020 - 0.1 - First Issue
#             18/10/2020 - 0.2 - Added the possibility to retrive the list of resources available

# Script Name & Version
NAME="mercedes_me_api.sh"
VERSION="0.1"

# Static Parameters
REDIRECT_URL="https://localhost"
SCOPE="mb:vehicle:mbdata:fuelstatus mb:vehicle:mbdata:vehiclestatus mb:vehicle:mbdata:vehiclelock offline_access"
STATE="12345678"
TOKEN_FILE=".mercedes_token"
CREDENTIALS_FILE=".mercedes_credentials"

# Credentials
CLIENT_ID=""
CLIENT_SECRET=""
VEHICLE_ID=""
# Loading Credentials
if [[ -f "$CREDENTIALS_FILE" ]]; then
  . $CREDENTIALS_FILE
fi
if [ -z $CLIENT_ID ] | [ -z $CLIENT_ID ] | [ -z $CLIENT_ID ]; then
  echo "Please create $CREDENTIALS_FILE with CLIENT_ID=\"\", CLIENT_SECRET=\"\", VEHICLE_ID=\"\""
  exit
fi

# URL
RES_URL="https://api.mercedes-benz.com/vehicledata/v2/vehicles/$VEHICLE_ID/resources"

# Resources
RES_FUEL=(rangeliquid tanklevelpercent)
RES_LOCK=(doorlockstatusvehicle doorlockstatusdecklid doorlockstatusgas positionHeading)
RES_STAT=(decklidstatus doorstatusfrontleft doorstatusfrontright doorstatusrearleft doorstatusrearright \
          interiorLightsFront interiorLightsRear lightswitchposition readingLampFrontLeft readingLampFrontRight \
          rooftopstatus sunroofstatus \
          windowstatusfrontleft windowstatusfrontright windowstatusrearleft windowstatusrearright
)

function usage ()
{
  echo "Usage:    $NAME <arguments>"
  echo
  echo "Example:  $NAME --token --fuel"
  echo "     or:  $NAME -l"
  echo
  echo "Arguments:"
  echo "    -t, --token        Procedure to obtatin the Access Token (stored into $TOKEN_FILE)"
  echo "    -r, --refresh      Procedure to refresh the Access Token (stored into $TOKEN_FILE)"
  echo "    -f, --fuel         Retrive the Fuel Status of your Vehicle"
  echo "    -l, --lock         Retrive the Lock Status of your Vehicle"
  echo "    -s, --status       Retrive the General Status of your Vehicle"
  echo "    -R, --resources    Retrive the list of available resources of your Vehicle"
  exit
}

function parse_options ()
{
	# Check Options
	OPT=$(getopt -o trflsR --long token,refresh,fuel,lock,status,resources -n "$NAME parse-error" -- "$@")
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
			--resources )
				printResources
				shift
				;;
			* ) shift ;;
		esac
	done
}

function generateBase64 ()
{
  BASE64=$(echo -n $CLIENT_ID:$CLIENT_SECRET | base64 | sed -r 's/ //')
  BASE64=$(echo $BASE64 | sed -r 's/ //')
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
  ACCESS_TOKEN=$(cat $TOKEN_FILE | sed -e "s/{//g;s/}//g" | sed -e "s/",/"\n/g" | sed -e "s/:/:\t/g" | grep access_token |awk '{print $2'} | sed -e "s/\"//g")
}

function extractRefreshToken ()
{
  REFRESH_CODE=$(cat $TOKEN_FILE | sed -e "s/{//g;s/}//g" | sed -e "s/",/"\n/g" | sed -e "s/:/:\t/g" | grep refresh_token |awk '{print $2'} | sed -e "s/\"//g")
}

function printStatus ()
{
  extractAccessToken

  for r in "$@"
    do
    echo "Retriving $r:"
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
