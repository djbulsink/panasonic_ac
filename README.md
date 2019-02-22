# Panasonic Comfort Cloud HA component

A home assistant custom climate component to control Panasonic airconditioners and heatpumps. 

This component uses the library `pcomfortcloud`

https://github.com/lostfields/python-panasonic-comfort-cloud

## Usage
Copy climate.py to the `custom_components/panasonc_ac/` folder. And add the following configuration in `configuration.yml` 

```yaml
climate:
  - platform: panasonic_ac
    username: !secret user
    password: !secret password
```
