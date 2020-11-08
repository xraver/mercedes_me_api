# mercedes_me_api 
[![License Status][license-img]][license-url]
[![Releases][releases-img]][releases-url]
[![Last Commit][last-commit-img]][last-commit-url]
[![hacs][hacs-img]][hacs-url]
[![BuyMeCoffee][buymecoffee-img]][buymecoffee-url]

Home Assistant Custom Component to integrate the sensors of a Mercedes-Benz car using [Mercedes Me APIs](https://developer.mercedes-benz.com/products).

## Pre-Requirements
1) Own a Mercedes Benz Car with Mercedes Me installed and working.
2) Create an application in https://developer.mercedes-benz.com/
3) Register to the following APIs:
   - [Fuel Status](https://developer.mercedes-benz.com/products/fuel_status)
   - [Vehicle Lock Status](https://developer.mercedes-benz.com/products/vehicle_lock_status)
   - [Vehicle Status](https://developer.mercedes-benz.com/products/vehicle_status)

Note: the APIs described above do not requires any subscription in case you use them with your own car associated the the Mercedes Me Account.
Note2: only one car is supported for the moment.

### Open Points
- Complete OAUTH2 Authentication & Get the First Token
- Get state after starts -> now it waits <scan_interval> seconds.
- Config Flow for automatic configuration
- ~~HACS~~
- Log Management
- Bugfix & Software optimizations

{% if not installed %}
### Installation
To use this custom component it's necessary to perform the following instructions:
1) clone the repository
2) create make a symbolic link from git_repost/custom_components/mercedesmeapi to hass_folder/custom_components

{% endif %}
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
[buymecoffee-url]: https://www.buymeacoffee.com/xraver
