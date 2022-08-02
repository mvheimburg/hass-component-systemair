"""Platform for newer SystemAir AC units with Modbus adapter."""
from __future__ import annotations

import logging
from typing import List
import asyncio
import voluptuous as vol
from functools import partial

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.climate import PLATFORM_SCHEMA, ClimateEntity, ClimateEntityDescription
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
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.const import (
    ATTR_TEMPERATURE,
    CONF_NAME,
    CONF_SLAVE,
    TEMP_CELSIUS,
    PRECISION_TENTHS,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback


from .const import *


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_HUB, default=DEFAULT_HUB): cv.string,
        vol.Required(CONF_SLAVE): vol.All(int, vol.Range(min=0, max=32)),
        vol.Optional(CONF_NAME, default=DOMAIN): cv.string,
    }
)

_LOGGER = logging.getLogger(__name__)


from pysystemair import PySystemAir, Callbacks
# from .pysystemair.const import USER_MODES


# async def async_setup_platform(
#     hass: HomeAssistant,
#     config: ConfigType,
#     async_add_entities,
#     discovery_info: DiscoveryInfoType | None = None,
# ):

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the SystemAir Platform."""
    modbus_slave = entry.data[CONF_SLAVE]
    name = entry.data[CONF_NAME]
    hub = get_hub(hass, DEFAULT_HUB)
    async_add_entities([SystemAir(hub, modbus_slave, name)], update_before_add=True)
    # return True

class SystemAir(ClimateEntity):
    """
    Class SystemAir used to represent a Systemair SAVE VTR unit.
    """
    _attr_hvac_modes = [HVACMode.HEAT, HVACMode.COOL, HVACMode.FAN_ONLY]
    _attr_hvac_mode = HVACMode.FAN_ONLY
    _attr_max_temp = 25
    _attr_min_temp = 15
    _attr_supported_features = ClimateEntityFeature.FAN_MODE | ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.TARGET_HUMIDITY | ClimateEntityFeature.PRESET_MODE
    _attr_target_temperature_step = PRECISION_TENTHS
    _attr_temperature_unit = TEMP_CELSIUS
    _attr_fan_modes = [FAN_OFF, FAN_LOW, FAN_MEDIUM, FAN_HIGH, FAN_AUTO]
    _attr_fan_mode = FAN_MEDIUM
    _attr_preset_modes = USER_MODES
    _attr_preset_mode = USER_MODES[1]

    def __init__(self, hub: ModbusHub, modbus_slave: int | None, name: str | None) -> None:
        """Initialize the unit."""
        self._hub = hub
        self._attr_name = name
        self._slave = modbus_slave
        callbacks = Callbacks(
                        holding_reg=partial(self._hub.async_pymodbus_call, unit=self._slave, value=1, use_call=CALL_TYPE_REGISTER_INPUT), 
                        input_reg=partial(self._hub.async_pymodbus_call, unit=self._slave, value=1, use_call=CALL_TYPE_REGISTER_HOLDING), 
                        write_reg=partial(self._hub.async_pymodbus_call, unit=self._slave, use_call=CALL_TYPE_WRITE_REGISTER))
        self._unit = PySystemAir(callbacks=callbacks)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN)},
            name=self._attr_name,
            manufacturer="SystemAir",
        )
        self._attr_extra_state_attributes={
            "filter_hours":             0,
            "filter_alarm":             0,
            "heat_exchanger_active":    0,
            "heat_exchanger":           0,
            # "heating": 0,
            "heater_enabled":           0,
            "free_cooling_enabled":     0,
            "free_cooling_active":      0,
            "free_cooling_start_time":  0,
            "free_cooling_end_time":    0,
            "outdoor_air_temp":         0,
        }
        _LOGGER.warning("SYSTEMAIR SAVE VTR COMPONENT SETUP")


    async def async_update(self) -> None:
        """Get the latest data."""
        await self._unit.async_update_all()
        self._attr_current_temperature = self._unit.current_temperature
        # _LOGGER.warning(f"self._attr_current_temperature: {self._attr_current_temperature}")
        self._attr_target_temperature = self._unit.target_temperature
        self._attr_current_humidity = self._unit.current_humidity
        self._attr_target_humidity = self._unit.target_humidity
        # _LOGGER.warning(f"self._attr_target_humidity: {self._attr_target_humidity}")
        self._attr_fan_mode = SYSTEMAIR_TO_HASS_FAN_MODES[self._unit.fan_mode]
        # _LOGGER.warning(f"self._attr_fan_mode: {self._attr_fan_mode}")

        self._attr_extra_state_attributes.update({
            "filter_hours":             self._unit.filter_hours,
            "filter_alarm":             self._unit.filter_alarm,
            "heat_exchanger_active":    self._unit.heat_exchanger_active,
            "heat_exchanger":           self._unit.heat_exchanger,
            # "heating": 0,
            "heater_enabled":           self._unit.heater_enabled,
            "free_cooling_enabled":     self._unit.free_cooling_enabled,
            "free_cooling_active":      self._unit.free_cooling_active,
            "free_cooling_start_time":  self._unit.free_cooling_start_time,
            "free_cooling_end_time":    self._unit.free_cooling_end_time,
            "outdoor_air_temp":         self._unit.outdoor_air_temp,
            })
        # self._attr_available = True

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
        _LOGGER.warning(f"Setting fan_mode: {fan_mode} with type: {type(fan_mode)}")
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