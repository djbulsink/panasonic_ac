# Panasonic Comfort Cloud HA component

A home assistant custom climate component to control Panasonic airconditioners and heatpumps.

This component uses the library `pcomfortcloud`

https://github.com/lostfields/python-panasonic-comfort-cloud

## Usage
Add the following configuration in `configuration.yaml`:

```yaml
climate:
  - platform: panasonic_ac
    username: !secret user
    password: !secret password
```
