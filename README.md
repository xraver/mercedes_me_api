# mercedes_me_api
[![Releases][releases-img]][releases-url]
[![Last Commit][last-commit-img]][last-commit-url]
[![hacs][hacs-img]][hacs-url]
[![License Status][license-img]][license-url]
[![BuyMeCoffee][buymecoffee-img]][buymecoffee-url]

This repository contains a collection of scripts (including the Home Assistant Custom Component) in order to collect data from the sensors of a Mercedes-Benz car using [Mercedes me API](https://developer.mercedes-benz.com/products).

## Pre-Requirements
1) Own a Mercedes Benz Car with Mercedes me installed and working.
2) Create an application in https://developer.mercedes-benz.com/
3) Register to the following APIs (all of them):
   - [Electric Vehicle Status](https://developer.mercedes-benz.com/products/electric_vehicle_status)
   - [Fuel Status](https://developer.mercedes-benz.com/products/fuel_status)
   - [Pay As You Drive Insurance](https://developer.mercedes-benz.com/products/pay_as_you_drive_insurance)
   - [Vehicle Lock Status](https://developer.mercedes-benz.com/products/vehicle_lock_status)
   - [Vehicle Status](https://developer.mercedes-benz.com/products/vehicle_status)

Notes:
1) the APIs described above do not require any subscription in case you use them with your own car associated with the Mercedes me Account.
2) not all sensors may be available in your own car; if a sensor is not available the data request returns no data.
3) only one car is supported for the moment.

## Home Assistant Custom Component
The Home Assistant Custom Component is a component to be added in Home Assistant in order to integrate the sensors of a Mercedes-Benz car using [Mercedes me API](https://developer.mercedes-benz.com/products).
This component is still in development.
### Open Points & Issues
- Complete OAUTH2 Authentication & Get the First Token
- Get state after starts -> now it waits <scan_interval> seconds.
- Config Flow for automatic configuration
- Log Management
- Bugfix & Software optimizations

For further details please refer to [issues list][issues-url].

### Installation
To use this custom component it's necessary to perform the following instructions:
1) clone the repository
2) create make a symbolic link from git_repost/custom_components/mercedesmeapi to hass_folder/custom_components

### Configuration
1) Add in the configuration.yaml the following emelents:
```yaml
mercedesmeapi:
  client_id: <**INSERT_YOUR_CLIENT_ID**>
  client_secret: <**INSERT_YOUR_CLIENT_SECRET**>
  vehicle_id: <**INSERT_YOUR_VEHICLE_ID**>
  enable_resources_file: <**ENABLE (true) OR DISABLE (false) RESOURCES - OPTIONAL (DEFAULT DISABLED)**>
  scan_interval: <** TIME PERIOD (NUMBER OF SECONDS) TO REFRESH RESOURCES - OPTIONAL**>
```
2) Actually it's not possible to retrieve the token from scratch. Please use the other scripts to retrieve the first token and copy it (.mercedesme_token) into the homeassistant configuration folder, in the same path where configuration.yaml is located

### Debug
To enable advanced log please expand the logger module configuration with the following lines:
```yaml
logger:
  logs:
    custom_components.mercedesmeapi: debug
```

## Shell Scripts
There are two shell script:
1) Python Version
2) Bash Version
The installation is the same, the usage is different.

## Installation
To use this script it's necessary to perform the following instructions:
1) clone the repository
2) create a config file (.mercedesme_config) with:
```bash
CLIENT_ID=<**INSERT_YOUR_CLIENT_ID**>
CLIENT_SECRET=<**INSERT_YOUR_CLIENT_SECRET**>
VEHICLE_ID=<**INSERT_YOUR_VEHICLE_ID**>
ENABLE_RESOURCES_FILE: <**ENABLE (true) OR DISABLE (false) RESOURCES - (DEFAULT DISABLED)**>
```

where CLIENT_ID and CLIENT_SECRET referring to the application information that can be found in [Mercedes Developer Console](https://developer.mercedes-benz.com/console) and VEHICLE_ID is the VIN of your car.

## First Token Creation
To create the first token it's necessary to perform the following steps:
1) Create the APP and register it to all APIs as describe in the Pre-Requirements paragraph
2) Logout in all browser from Mercedes Me (Developer site included)
3) Execute the shell or python script with -t parameter to obrain the first token
4) Open with a browser the link provided by the script: a login page will be shown
5) Using your Mercedes Me credential log in: a new web-page will ask to authorize the APP created in the step 1 to access to the personal information associated to the APIs registered
6) Enable all information and press Allow
7) An error page will appear: check the URI: it's something like https://localhost/?code=DQ8htZSw4WtJ27r7sTrVJwszGWxrCx9emy5FDUFa
8) Copy the part of the URI after code= (in this case DQ8htZSw4WtJ27r7sTrVJwszGWxrCx9emy5FDUFa) and paste into the running script

### Python Usage
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

### Bash Usage
To execute the script read below:
```bash
Usage:    mercedes_me_api.sh <arguments>

Example:  mercedes_me_api.sh --token --fuel
     or:  mercedes_me_api.sh -l

Arguments:
    -t, --token           Procedure to obtatin the Access Token (stored into .mercedesme_token)
    -r, --refresh         Procedure to refresh the Access Token (stored into .mercedesme_token)
    -f, --fuel            Retrieve the Fuel Status of your Vehicle
    -l, --lock            Retrieve the Lock Status of your Vehicle
    -s, --status          Retrieve the General Status of your Vehicle
    -e, --electric-status Retrieve the General Electric Status of your Vehicle
    -o, --odometer        Retrieve the Odometer reading of your Vehicle
    -R, --resources       Retrieve the list of available resources of your Vehicle
```

## Change Log
You can find change log under [releases][releases-url]

## License
[MIT](http://opensource.org/licenses/MIT) © Giorgio Ravera

## Donate
[![BuyMeCoffee][buymecoffee-button]][buymecoffee-url]

---

[license-img]: https://img.shields.io/github/license/xraver/mercedes_me_api
[license-url]: LICENSE
[issues-url]: https://github.com/xraver/mercedes_me_api/issues
[releases-img]: https://img.shields.io/github/v/release/xraver/mercedes_me_api
[releases-url]: https://github.com/xraver/mercedes_me_api/releases
[last-commit-img]: https://img.shields.io/github/last-commit/xraver/mercedes_me_api
[last-commit-url]: https://github.com/xraver/mercedes_me_api/commits/master
[hacs-img]: https://img.shields.io/badge/HACS-Default-orange.svg
[hacs-url]: https://github.com/custom-components/hacs
[buymecoffee-img]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg
[buymecoffee-button]: https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg
[buymecoffee-url]: https://www.buymeacoffee.com/raverag
