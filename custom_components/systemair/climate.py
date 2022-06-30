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
    HVAC_MODE_COOL,
    SUPPORT_FAN_MODE,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_TARGET_HUMIDITY,
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

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE | SUPPORT_FAN_MODE | SUPPORT_TARGET_HUMIDITY

from .pysystemair.pysystemair import PySystemAir


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities,
    discovery_info: DiscoveryInfoType = None,
):
    """Set up the SystemAir Platform."""
    # modbus_slave = config.get(CONF_SLAVE)

    # if discovery_info is None:  # pragma: no cover
    #     return

    # name = config.get(CONF_NAME)
    # hub = hass.data[MODBUS_DOMAIN][config.get(CONF_HUB)]
    # hub = hass.data[MODBUS_DOMAIN][config.get(CONF_HUB)]
    hub = get_hub(hass, config[CONF_HUB])
    # async_add_entities([SystemAir(hub, modbus_slave, name)], True)
    async_add_entities([SystemAir(hub, config)], True)
    
    return True

# async def async_setup_entry(hass, config_entry, async_add_entities):
#     """Set up the Demo SystemAir entry."""
#     await async_setup_platform(hass, {}, async_add_entities)


class SystemAir(ClimateEntity):
    """
    Class SystemairSave used to represent a Systemair SAVE VTR unit.
    Attributes
    ----------
    _input_regs : dict
        A dictionary with input registers.
    _holding_regs : dict
        A dictionary with holding registers.
    _slave : int
        Slave number of the unit.
    _conn : ModbusClient
        Modbus client (pymodbus.client) used to communicate with the unit.
    """

    def __init__(
        self, 
        hub: ModbusHub, 
        # modbus_slave, 
        config):
        """Initialize the unit."""


        self._hub = hub
        self._name = config.get(CONF_NAME)
        self._slave = config.get(CONF_SLAVE)

        self._unit = PySystemAir(
                     async_callback_holding_reg=partial(self._hub.async_pymodbus_call, unit=self._slave, value=1, use_call=CALL_TYPE_REGISTER_INPUT)
                    ,async_callback_input_reg=partial(self._hub.async_pymodbus_call, unit=self._slave, value=1, use_call=CALL_TYPE_REGISTER_HOLDING)
                    ,async_callback_write_reg=partial(self._hub.async_pymodbus_call, unit=self._slave, use_call=CALL_TYPE_WRITE_REGISTER))


        self._fan_modes = ["Off", "Low", "Normal", "High"]

        # self._input_regs = REGMAP_INPUT
        # self._holding_regs = REGMAP_HOLDING

        self._current_operation = None
        # self._setpoint_temp_max = None
        # self._setpoint_temp_min = None
        # self._current_humidity = None
        # self._setpoint_humidity = None
        # self._supply_temp = None
        # self._extract_temp = None
        # self._outdoor_temp = None
        self._user_mode = None
        # self._heater = None
        # self._heater_state = None
        # self._filter_warning = None
        # self._filter_hours = None
        # self._thermal_exchange_heat_enabled = None
        # self._thermal_exchange_heat_state = None
        # self._thermal_exchange_cold_enabled = None
        # self._thermal_exchange_cold_state = None
        # self._fan_speed_supply = None
        # self._fan_speed_extract = None

        # self._update_on_read = UPDATE_ON_READ
        # self._fan_can_turn_off = None

        _LOGGER.warning("SAVE VTR COMPONENT SETUP")
        # self.min_humidity = 20
        # self.max_humidity = 50
        # self.state = 'on'

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS



    # async def async_update(self):
    #     """
    #     Updates all of the input and holding regs dict values.
    #     """
    #     ret = True
    #     try:
    #         for k in self._input_regs:
    #             await self.async_update_from_register("input", k)
    #             # self._input_regs[k]["value"] = self._hub.read_input_registers(
    #             #     unit=self._slave, address=self._input_regs[k]["addr"], value=1
    #             # ).registers
    #         for k in self._holding_regs:
    #             await self.async_update_from_register("holding", k)
    #             # self._holding_regs[k]["value"] = self._hub.read_holding_registers(
    #             #     unit=self._slave, address=self._holding_regs[k]["addr"], value=1
    #             # ).registers
    #     except AttributeError:
    #         # The unit does not reply reliably
    #         ret = False
    #         print("Modbus read failed")


    # async def async_update_from_register(self, reg_type, variable):
    #     """
    #     Updates all of the input and holding regs dict values.
    #     """
    #     try:
    #         if reg_type == "input":
    #             result = await self._hub.async_pymodbus_call(
    #                 unit=self._slave, address=self._input_regs[variable]["addr"], value=1, use_call=CALL_TYPE_REGISTER_INPUT)
    #             if result is None:
    #                 _LOGGER.warning(f"Error reading {variable} value from SystemAir modbus adapter")
    #             else:
    #                 self._input_regs[variable]["value"] = result.registers[0]


    #         elif reg_type == "holding":
    #             result = await self._hub.async_pymodbus_call(
    #                 unit=self._slave, address=self._holding_regs[variable]["addr"], value=1, use_call=CALL_TYPE_REGISTER_HOLDING)
    #             if result is None:
    #                 _LOGGER.warning(f"Error reading {variable} value from SystemAir modbus adapter")
    #             else:
    #                 self._holding_regs[variable]["value"] = result.registers[0]

    #     except AttributeError as e:
    #         # The unit does not reply reliably
    #         # ret = False
    #         # _LOGGER.warning("Modbus read failed")
    #         raise e
        

    @staticmethod
    def get_twos_comp(argument):
        if argument > 32767:
            return -(65535 - argument)
        else:
            return argument

    @staticmethod
    def get_user_mode_switch(argument):
        switcher = {
            0: "Auto",
            1: "Manual",
            2: "Crowded",
            3: "Refresh",
            4: "Fireplace",
            5: "Away",
            6: "Holiday",
            7: "Cooker Hood",
            8: "Vacuum Cleaner",
            9: "CDI1",
            11: "CDI2",
            12: "PressureGuard",
        }
        return switcher.get(argument, "nothing")

    @property
    def hvac_mode(self):
        """Return current operation ie. heat, cool, idle."""
        return self._current_operation

    @property
    def hvac_modes(self) -> List[str]:
        """Return the list of available hvac operation modes.

        Need to be a subset of HVAC_MODES.
        """
        return HVAC_MODES

    @property
    def name(self):
        """Return the name of the climate device."""
        return self._name

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def fan_mode(self):
        """Return the fan setting."""
        # if self._update_on_read:
        #     await self.update_from_register("holding", "fan_mode")
        return self._fan_modes[self._holding_regs["fan_mode"]["value"] - 1]

    @property
    def fan_modes(self):
        """Return the list of available fan modes."""
        return self._fan_modes

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        # if self._update_on_read:
        #     await self.update_from_register("input", "target_temperature")
        return self._unit.target_temperature()

    @property
    def current_temperature(self):
        """Return the current temperature."""
        # if self._update_on_read:
        #     await self.update_from_register("holding", "supply_air_temperature")
        return self._holding_regs["supply_air_temperature"]["value"] / 10

    @property
    def current_humidity(self):
        """Return the temperature we try to reach."""
        # if self._update_on_read:
        #     await self.update_from_register("holding", "humidity")
        return self._holding_regs["humidity"]["value"]

    @property
    def target_humidity(self):
        """Return the temperature we try to reach."""
        # if self._update_on_read:
        #     await self.update_from_register("holding", "target_humidity")
        return self._holding_regs["target_humidity"]["value"]

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        if kwargs.get(ATTR_TEMPERATURE) is not None:
            target_temperature = kwargs.get(ATTR_TEMPERATURE)
            target_temperature=int(round(target_temperature*10))
            _LOGGER.warning(f"Setting temp: {target_temperature} with type: {type(target_temperature)}")
            if await self._hub.async_pymodbus_call(
            unit=self._slave,
            address=(self._holding_regs["target_temperature"]["addr"]),
            value=target_temperature,
            use_call=CALL_TYPE_WRITE_REGISTER):
                self._holding_regs["target_temperature"]["value"] = target_temperature
            else:
                _LOGGER.error("Unable to set tempereatur to SystemAir modbus interface")
        else:
            _LOGGER.error("Errounous tempereatur to SystemAir")


    async def async_set_fan_mode(self, fan_mode):
        """Set new fan mode."""
        fan_value = self._fan_modes.index(fan_mode) + 1
        _LOGGER.warning(f"Setting fan_value: {fan_value} with type: {type(fan_value)}")
        if await self._hub.async_pymodbus_call(
        unit=self._slave,
        address=(self._holding_regs["fan_mode"]["addr"]),
        value=fan_value,
        use_call=CALL_TYPE_WRITE_REGISTER):
            self._holding_regs["fan_mode"]["value"] = fan_value
        else:
             _LOGGER.error("Unable to set tempereatur to SystemAir modbus interface")
  
    # async def set_humidity(self, **kwargs):
    #     pass

    async def async_set_humidity(self, humidity):
        """Set new target temperature."""
    #    if kwargs.get(ATTR_HUMIDITY) is not None:
    #        target_humidity = kwargs.get(ATTR_HUMIDITY, 30)
        target_humidity=int(round(humidity))
        _LOGGER.warning(f"Setting humidity: {target_humidity} with type: {type(target_humidity)}")
        if await self._hub.async_pymodbus_call(
           unit=self._slave,
           address=(self._holding_regs["target_humidity"]["addr"]),
           value=target_humidity,
           use_call=CALL_TYPE_WRITE_REGISTER):
            self._holding_regs["target_humidity"]["value"] = target_humidity
        else:
             _LOGGER.error("Unable to set tempereatur to SystemAir modbus interface")