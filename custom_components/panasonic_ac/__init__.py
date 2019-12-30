
import logging
import voluptuous as vol
from datetime import timedelta
from typing import Any, Dict, Optional, List
import homeassistant.helpers.config_validation as cv

from homeassistant.const import CONF_USERNAME, CONF_PASSWORD

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


DOMAIN = 'panasonic_ac'
COMPONENT_TYPES = ["climate", "sensor"]

def setup(hass: HomeAssistantType, hass_config: ConfigType) -> bool:
    import pcomfortcloud

    """Set up the panasonic cloud components."""
    username = hass_config.get(CONF_USERNAME)
    password = hass_config.get(CONF_PASSWORD)

    api = pcomfortcloud.Session(username, password, verifySsl=False)
    try:
        api.login()
    except:
        return False
    
    load_platform(hass, "climate", DOMAIN, {}, hass_config)
    #load_platform(hass, "sensor", DOMAIN, {}, hass_config)
    return True

