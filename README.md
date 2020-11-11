# mercedes_me_api 
[![License Status][license-img]][license-url]
[![Releases][releases-img]][releases-url]
[![Last Commit][last-commit-img]][last-commit-url]
[![hacs][hacs-img]][hacs-url]
[![BuyMeCoffee][buymecoffee-img]][buymecoffee-url]

Script to use Mercedes Me APIs.

## Pre-Requirements
1) Own a Mercedes Benz Car with Mercedes Me installed and working.
2) Create an application in https://developer.mercedes-benz.com/
3) Register to the following APIs:
   - [Fuel Status](https://developer.mercedes-benz.com/products/fuel_status)
   - [Vehicle Lock Status](https://developer.mercedes-benz.com/products/vehicle_lock_status)
   - [Vehicle Status](https://developer.mercedes-benz.com/products/vehicle_status)

Note: the APIs described above do not requires any subscription in case you use them with your own car associated the the Mercedes Me Account.
Note2: only one car is supported for the moment.

## Home Assistant Custom Component
The Home Assistant Custom Component is a component to be added in Home Assistant in order to integrate the sensors of a Mercedes-Benz car using [Mercedes Me API](https://developer.mercedes-benz.com/products).
This component is still in development.
### Open Points
- Complete OAUTH2 Authentication & Get the First Token
- Get state after starts -> now it waits <scan_interval> seconds.
- Config Flow for automatic configuration
- Log Management
- Bugfix & Software optimizations

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
  scan_interval: <** TIME PERIOD TO REFRESH RESOURCES **>
```
2) Actually it's not possible to retrive the Token from scratch. Please use the other script to retrive the first token and copy it into hacs folder (.mercedesme_token)

## Shell Scripts
There are two shell script:
1) Python Version
2) Bash Version
The installation is the same, the usage is different.

## Installation
To use this script it's necessary to perform the following instructions:
1) clone the repository
2) create a credentials files (.mercedesme_credentials) with:
```bash
CLIENT_ID=<**INSERT_YOUR_CLIENT_ID**>
CLIENT_SECRET=<**INSERT_YOUR_CLIENT_SECRET**>
VEHICLE_ID=<**INSERT_YOUR_VEHICLE_ID**>
```

where CLIENT_ID and CLIENT_SECRET referring to the application information that can be found in [Mercedes Developer Console](https://developer.mercedes-benz.com/console) and VEHICLE_ID is the VIN of your car.

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

The possible arguments are:
    -t, --token        Procedure to obtatin the Access Token (stored into .mercedesme_token)
    -r, --refresh      Procedure to refresh the Access Token (stored into .mercedesme_token)
    -f, --fuel         Retrive the Fuel Status of your Vehicle
    -l, --lock         Retrive the Lock Status of your Vehicle
    -s, --status       Retrive the General Status of your Vehicle
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
[releases-img]: https://img.shields.io/github/v/release/xraver/mercedes_me_api
[releases-url]: https://github.com/xraver/mercedes_me_api/releases
[last-commit-img]: https://img.shields.io/github/last-commit/xraver/mercedes_me_api
[last-commit-url]: https://github.com/xraver/mercedes_me_api/commits/master
[hacs-img]: https://img.shields.io/badge/HACS-Custom-orange.svg
[hacs-url]: https://github.com/custom-components/hacs
[buymecoffee-img]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg
[buymecoffee-button]: https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg
[buymecoffee-url]: https://www.buymeacoffee.com/raverag
