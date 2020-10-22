# mercedes_me_api [![License Status](https://img.shields.io/github/license/xraver/mercedes_me_api)](https://github.com/xraver/mercedes_me_api/blob/master/LICENSE) [![Tag Status](https://img.shields.io/github/v/tag/xraver/mercedes_me_api)](https://github.com/xraver/mercedes_me_api/tags) [![Last Commit](https://img.shields.io/github/last-commit/xraver/mercedes_me_api)](https://github.com/xraver/mercedes_me_api/commits/master)
Script to interface with Mercedes Me APIs

## Pre-Requirements
1) Own a Mercedes Benz Car with Mercedes Me installed and working.
2) Create an application in https://developer.mercedes-benz.com/
3) Register to the following APIs:
   - [Fuel Status](https://developer.mercedes-benz.com/products/fuel_status)
   - [Vehicle Lock Status](https://developer.mercedes-benz.com/products/vehicle_lock_status)
   - [Vehicle Status](https://developer.mercedes-benz.com/products/vehicle_status)

Note: the APIs described above do not requires any subscription in case you use them with your own car associated the the Mercedes Me Account.

## Installation
To use this script it's necessary to perform the following instructions:
1) clone the repository
2) create a credentials files (.mercedes_credentials) with:
```bash
CLIENT_ID=<**INSERT_YOUR_CLIENT_ID**>
CLIENT_SECRET=<**INSERT_YOUR_CLIENT_SECRET**>
VEHICLE_ID=<**INSERT_YOUR_VEHICLE_ID**>
```

where CLIENT_ID and CLIENT_SECRET referring to the application information that can be found in [Mercedes Developer Console](https://developer.mercedes-benz.com/console) and VEHICLE_ID is the VIN of your car.

## Python Usage
To execute the script read below:
```bash
usage: mercedes_me_api.py [-h] [-t] [-r] [-s] [-R] [-v]

optional arguments:
  -h, --help       show this help message and exit
  -t, --token      Procedure to obtatin the Access Token
  -r, --refresh    Procedure to refresh the Access Token
  -s, --status     Retrive the Status of your Vehicle
  -R, --resources  Retrive the list of available resources of your Vehicle
  -v, --version    show program's version number and exit
```

## Bash Usage
To execute the script read below:
```bash
Usage:    mercedes_me_api.sh <arguments>

Example:  mercedes_me_api.sh --token --fuel
     or:  mercedes_me_api.sh -l

The possible arguments are:
    -t, --token        Procedure to obtatin the Access Token (stored into .mercedes_token)
    -r, --refresh      Procedure to refresh the Access Token (stored into .mercedes_token)
    -f, --fuel         Retrive the Fuel Status of your Vehicle
    -l, --lock         Retrive the Lock Status of your Vehicle
    -s, --status       Retrive the General Status of your Vehicle
```

## License
[MIT](http://opensource.org/licenses/MIT) © Giorgio Ravera

## Donate
If you want to offer me a coffee:

[![paypal](https://www.paypalobjects.com/en_US/IT/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=giorgio.ravera%40gmail.com&currency_code=EUR)
