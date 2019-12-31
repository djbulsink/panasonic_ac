"""
Support for Panasonic comfortcloud integration.
"""
import logging
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import load_platform
from homeassistant.helpers.typing import ConfigType, HomeAssistantType
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD

DOMAIN = 'panasonic_ac'
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

COMPONENT_TYPES = ["climate"]
_LOGGER = logging.getLogger(__name__)

def setup(hass, config) -> bool:
    import pcomfortcloud
    _LOGGER.info('setup panasonic ac')
    """Set up the panasonic cloud components."""
    username = config[DOMAIN][CONF_USERNAME]
    password = config[DOMAIN][CONF_PASSWORD]

    api = pcomfortcloud.Session(username, password, verifySsl=False)
    api.login()

    hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["api"] = api

    load_platform(hass, "climate", DOMAIN, {}, config)
    #load_platform(hass, "sensor", DOMAIN, {}, config)
    return True
