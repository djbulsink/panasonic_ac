# Panasonic Comfort Cloud HA component

A home assistant custom climate component to control Panasonic airconditioners and heatpumps.

This component uses the library `pcomfortcloud`

https://github.com/lostfields/python-panasonic-comfort-cloud

## Usage
- Copy `__init__.py`, `climate.py`, and `manifest.json` to the `custom_components/panasonic_ac/` folder. As an alternative, you can also install the component via the [Home Assistant Community Store (HACS)](https://hacs.netlify.com/) by adding it manually.
- Add the following configuration in `configuration.yaml`:

```yaml

panasonic_ac:
  username: !secret user
  password: !secret password
```
