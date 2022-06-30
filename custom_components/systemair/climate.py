"""Platform for newer SystemAir AC units with Modbus adapter."""
import logging
from typing import List
import asyncio
import voluptuous as vol
from functools import partial

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from homeassistant.components.climate import PLATFORM_SCHEMA, ClimateEntity
from homeassistant.components.climate.const import (
    # HVAC_MODE_COOL,
    # HVAC_MODE_HEAT,
    SUPPORT_FAN_MODE,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_TARGET_HUMIDITY,
    ClimateEntityFeature,
    HVACMode,
)

from homeassistant.components.modbus.modbus import ModbusHub

from homeassistant.components.modbus.const import (
    CONF_HUB, 
    DEFAULT_HUB, 
    MODBUS_DOMAIN,
    CALL_TYPE_REGISTER_HOLDING,
    CALL_TYPE_REGISTER_INPUT,
    CALL_TYPE_WRITE_REGISTER
)

from homeassistant.components.modbus import get_hub
from homeassistant.components.modbus.base_platform import BasePlatform

from homeassistant.const import (
    ATTR_TEMPERATURE,
    CONF_NAME,
    CONF_SLAVE,
    TEMP_CELSIUS,
    PRECISION_TENTHS,
)
import homeassistant.helpers.config_validation as cv



from .const import *


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_HUB, default=DEFAULT_HUB): cv.string,
        vol.Required(CONF_SLAVE): vol.All(int, vol.Range(min=0, max=32)),
        vol.Optional(CONF_NAME, default=DEVICE_DEFAULT_NAME): cv.string,
    }
)

_LOGGER = logging.getLogger(__name__)


from .pysystemair.pysystemair import PySystemAir


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities,
    discovery_info: DiscoveryInfoType | None = None,
):
    """Set up the SystemAir Platform."""
    modbus_slave = config.get(CONF_SLAVE)
    name = config.get(CONF_NAME)
    hub = get_hub(hass, config[CONF_HUB])
    async_add_entities([SystemAir(hub, modbus_slave, name)], True)
    


class SystemAir(ClimateEntity):
    """
    Class SystemAir used to represent a Systemair SAVE VTR unit.
    """
    _attr_hvac_modes = [HVACMode.HEAT, HVACMode.COOL, HVACMode.FAN_ONLY]
    _attr_hvac_mode = HVACMode.FAN_ONLY
    _attr_max_temp = 25
    _attr_min_temp = 15
    _attr_supported_features = ClimateEntityFeature.FAN_MODE | ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.TARGET_HUMIDITY
    _attr_target_temperature_step = PRECISION_TENTHS
    _attr_temperature_unit = TEMP_CELSIUS
    _attr_fan_modes = [FAN_OFF, FAN_LOW, FAN_MEDIUM, FAN_HIGH, FAN_AUTO]
    _attr_fan_mode = FAN_MEDIUM

    def __init__(hub: ModbusHub, modbus_slave: int | None, name: str | None
    ) -> None:
        """Initialize the unit."""
        self._hub = hub
        self._name = name
        self._slave = modbus_slave
        self._unit = PySystemAir(
                     async_callback_holding_reg=partial(self._hub.async_pymodbus_call, unit=self._slave, value=1, use_call=CALL_TYPE_REGISTER_INPUT)
                    ,async_callback_input_reg=partial(self._hub.async_pymodbus_call, unit=self._slave, value=1, use_call=CALL_TYPE_REGISTER_HOLDING)
                    ,async_callback_write_reg=partial(self._hub.async_pymodbus_call, unit=self._slave, use_call=CALL_TYPE_WRITE_REGISTER))


        _LOGGER.warning("SAVE VTR COMPONENT SETUP")


    async def async_update(self) -> None:
        """Get the latest data."""
        await self._unit.async_update_all()
        self._attr_current_temperature = self._unit.current_temperature
        self._attr_target_temperature = self._unit.target_temperature
        self._attr_current_humidity = self._unit.current_humidity
        self._attr_target_humidity = self._unit.target_humidity
        self._attr_fan_mode = SYSTEMAIR_TO_HASS_FAN_MODES[self._unit.fan_mode]
 

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        if kwargs.get(ATTR_TEMPERATURE) is not None:
            target_temperature = kwargs.get(ATTR_TEMPERATURE)
            target_temperature=int(round(target_temperature*10))
            _LOGGER.warning(f"Setting temp: {target_temperature} with type: {type(target_temperature)}")
            await self._unit.async_set_temperature(target_temperature)
        #     if await self._hub.async_pymodbus_call(
        #     unit=self._slave,
        #     address=(self._holding_regs["target_temperature"]["addr"]),
        #     value=target_temperature,
        #     use_call=CALL_TYPE_WRITE_REGISTER):
        #         self._holding_regs["target_temperature"]["value"] = target_temperature
            # else:
            #     _LOGGER.error("Unable to set tempereatur to SystemAir modbus interface")
        else:
            _LOGGER.error("Errounous tempereatur to SystemAir")


    async def async_set_fan_mode(self, fan_mode):
        """Set new fan mode."""
        # fan_value = self._fan_modes.index(fan_mode) + 1
        _LOGGER.warning(f"Setting fan_value: {fan_value} with type: {type(fan_value)}")
        await self._unit.async_set_fan_mode(HASS_TO_SYSTEMAIR_FAN_MODES[fan_mode])
        # if await self._hub.async_pymodbus_call(
        # unit=self._slave,
        # address=(self._holding_regs["fan_mode"]["addr"]),
        # value=fan_value,
        # use_call=CALL_TYPE_WRITE_REGISTER):
        #     self._holding_regs["fan_mode"]["value"] = fan_value
        # else:
        #      _LOGGER.error("Unable to set tempereatur to SystemAir modbus interface")
  
    # async def set_humidity(self, **kwargs):
    #     pass

    async def async_set_humidity(self, humidity):
        """Set new target temperature."""
    #    if kwargs.get(ATTR_HUMIDITY) is not None:
    #        target_humidity = kwargs.get(ATTR_HUMIDITY, 30)
        target_humidity=int(round(humidity))
        _LOGGER.warning(f"Setting humidity: {target_humidity} with type: {type(target_humidity)}")
        await self._unit.async_set_humidity(target_humidity)
        # if await self._hub.async_pymodbus_call(
        #    unit=self._slave,
        #    address=(self._holding_regs["target_humidity"]["addr"]),
        #    value=target_humidity,
        #    use_call=CALL_TYPE_WRITE_REGISTER):
        #     self._holding_regs["target_humidity"]["value"] = target_humidity
        # else:
        #      _LOGGER.error("Unable to set tempereatur to SystemAir modbus interface")