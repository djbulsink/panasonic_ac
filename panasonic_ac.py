import logging
import voluptuous as vol
import datetime
from homeassistant.components.climate import (
    ClimateDevice, STATE_HEAT, STATE_COOL,
    STATE_AUTO, STATE_DRY, STATE_FAN_ONLY,
    SUPPORT_TARGET_TEMPERATURE, SUPPORT_FAN_MODE, 
    SUPPORT_OPERATION_MODE, SUPPORT_SWING_MODE,
    SUPPORT_ON_OFF, PLATFORM_SCHEMA)
import homeassistant.helpers.config_validation as cv
from homeassistant.const import TEMP_CELSIUS, ATTR_TEMPERATURE

_LOGGER = logging.getLogger(__name__)
REQUIREMENTS = ['pcomfortcloud==0.0.13']

CONF_USERNAME = 'username'
CONF_PASSWORD = 'password'

SCAN_INTERVAL = datetime.timedelta(minutes=2)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})

OPERATION_LIST = {
    STATE_HEAT: 'Heat',
    STATE_COOL: 'Cool',
    STATE_AUTO: 'Auto',
    STATE_DRY: "Dry",
    STATE_FAN_ONLY: 'Fan' 
    }

SUPPORT_FLAGS = (SUPPORT_TARGET_TEMPERATURE | SUPPORT_FAN_MODE
                 | SUPPORT_OPERATION_MODE | SUPPORT_SWING_MODE 
                 | SUPPORT_ON_OFF )

import pcomfortcloud
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Dyson fan components."""
    
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)

    api = pcomfortcloud.Session(username, password, verifySsl=False )
    api.login()
    # Get panasonic Devices from api.
    _LOGGER.debug("Add panasonic devices")
    add_devices(
        [PanasonicDevice(device, api)
         for device in api.get_devices()], True
    )


class PanasonicDevice(ClimateDevice):
    """Representation of a Panasonic airconditioning."""

    def __init__(self, device, api):
        """Initialize the device."""
        _LOGGER.debug("Add panasonic device '{0}'".format(device['name']))
        self._api = api
        self._device = device
        self._current_temp = None
        self._is_on = False
        self._current_operation = 'Cool'

        self._unit = TEMP_CELSIUS
        self._cur_temp = None
        self._outside_temp = None
        self._target_temp = None
        self._mode = None
        self._eco = None

        self._current_fan = None
        self._airswing_hor = None
        self._airswing_vert = None
 
    def update(self):
        
        """Update the state of this climate device."""
        data= self._api.get_device(self._device['id'])
        
        if data is None:
            _LOGGER.debug("Received no data for device {id}".format(**self._device))
            return

        if data['parameters']['temperatureInside'] != 126:
            self._cur_temp = data['parameters']['temperatureInside']
        
        if data['parameters']['temperatureOutside'] != 126:
            self._outside_temp = data['parameters']['temperatureOutside']
        
        if data['parameters']['temperature'] != 126:
            self._target_temp = data['parameters']['temperature']
        
        self._is_on =bool( data['parameters']['power'].value )
        self._current_operation = data['parameters']['mode'].name
        self._current_fan = data['parameters']['fanSpeed'].name
        self._airswing_hor = data['parameters']['airSwingHorizontal'].name
        self._airswing_vert = data['parameters']['airSwingVertical'].name
        self._eco = data['parameters']['eco'].name


    @property
    def is_on(self):
        """Return is device is on."""
        return self._is_on        

    @property
    def current_operation(self):
        """Return the current operation."""
        return self._current_operation
    
    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    @property
    def name(self):
        """Return the display name of this climate."""
        return self._device['name']

    @property
    def group(self):
        """Return the display group of this climate."""
        return self._device['group']

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._cur_temp

    @property
    def target_temperature(self):
        """Return the target temperature."""
        return self._target_temp

    @property
    def operation_list(self):
        """Return the list of available operation modes."""
        return list(OPERATION_LIST.values())

    @property
    def current_fan_mode(self):
        """Return the fan setting."""
        return self._current_fan

    @property
    def fan_list(self):
        """Return the list of available fan modes."""
        return [f.name for f in pcomfortcloud.constants.FanSpeed ]

    @property
    def current_swing_mode(self):
        """Return the fan setting."""
        return self._airswing_hor

    @property
    def swing_list(self):
        """Return the list of available swing modes."""
        return [f.name for f in pcomfortcloud.constants.AirSwingUD ]

    def set_temperature(self, **kwargs):
        

        """Set new target temperature."""
        target_temp = kwargs.get(ATTR_TEMPERATURE)
        if target_temp is None:
            return
        
        _LOGGER.debug("Set %s temperature %s", self.name, target_temp)
        self._api.login()
        self._api.set_device(
            self._device['id'],
            power = pcomfortcloud.constants.Power.On,
            temperature = target_temp
        )

    def set_fan_mode(self, fan_mode):
        """Set new fan mode."""
        _LOGGER.debug("Set %s focus mode %s", self.name, fan_mode)
        self._api.login()
        self._api.set_device(
            self._device['id'],
            fanSpeed = pcomfortcloud.constants.FanSpeed[fan_mode]
        )

    def set_operation_mode(self, operation_mode):
        """Set operation mode."""
        _LOGGER.debug("Set %s heat mode %s", self.name, operation_mode)
        self._api.login()
        self._api.set_device(
            self._device['id'],
            mode = pcomfortcloud.constants.OperationMode[OPERATION_LIST[operation_mode]]
        )

    def turn_on(self):
        """Turn device on."""
        self._api.login()
        self._api.set_device(
            self._device['id'],
            power = pcomfortcloud.constants.Power.On
        )

    def turn_off(self):
        """Turn device on."""
        self._api.login()
        self._api.set_device(
            self._device['id'],
            power = pcomfortcloud.constants.Power.Off
        )

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        return 1

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return 37