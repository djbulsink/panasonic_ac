"""Platform for sensor integration."""
import logging
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

from . import DOMAIN


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return

    api = hass.data[DOMAIN].get('api')
    devices = []
    for device in api.get_devices():
        devices.append(OutsideTempSensor(device))

    add_entities(devices, True)

class OutsideTempSensor(Entity):
    """Representation of a sensor."""

    def __init__(self, device):
        """Initialize the sensor."""
        _LOGGER.debug("Add sensor for device '{0}'".format(device['name']))
        self._device = device
        self._state = None
        #self.hass.data[DOMAIN][self._device['id']] = { 'outside_temp' : None }

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Outside temperature "  + self._device['name']

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self):
        """Fetch new state data for the sensor."""
        _LOGGER.debug("{}".format(self.hass.data[DOMAIN]))
        try:
            self._state = self.hass.data[DOMAIN][self._device['id']]['outside_temp']
        except KeyError:
            self._state = None
