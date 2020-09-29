# mercedes_me_api
Script to interface with Mercedes Me APIs

# Pre-Requirements
1) Own a Mercedes Benz Car with Mercedes Me installed and working.
2) Create an application in https://developer.mercedes-benz.com/
3) Register to the following APIs:
   - [Fuel Status](https://developer.mercedes-benz.com/products/fuel_status)
   - [Vehicle Lock Status](https://developer.mercedes-benz.com/products/vehicle_lock_status)
   - [Vehicle Status](https://developer.mercedes-benz.com/products/vehicle_status)

Note: the APIs described above do not requires any subscription in case you use them with your own car associated the the Mercedes Me Account.

# Installation
To use this script it's necessary to perform the following instructions:
1) clone the repository
2) create a credentials files (.mercedes_credentials) with:
> CLIENT_ID=""

> CLIENT_SECRET=""

> VEHICLE_ID=""

where CLIENT_ID and CLIENT_SECRET referring to the application information that can be found in [Mercedes Developer Console](https://developer.mercedes-benz.com/console) and VEHICLE_ID is the VIN of your car.


# Usage
To execute the script the command is:

> $ ./mercedes_me_api.sh <arguments>

The possible arguments are:

>    -t, --token        Procedure to obtatin the Access Token (stored into .mercedes_token)
    
>    -r, --refresh      Procedure to refresh the Access Token (stored into .mercedes_token)
    
>    -f, --fuel         Retrive the Fuel Status of your Vehicle
    
>    -l, --lock         Retrive the Lock Status of your Vehicle
    
>    -s, --status       Retrive the General Status of your Vehicle
