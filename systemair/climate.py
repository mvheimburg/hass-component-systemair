"""Platform for newer SystemAir AC units with Modbus adapter."""
import logging
from typing import List

import voluptuous as vol

from homeassistant.components.climate import PLATFORM_SCHEMA, ClimateEntity
from homeassistant.components.climate.const import (
    HVAC_MODE_COOL,
    SUPPORT_FAN_MODE,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_TARGET_HUMIDITY,
)
from homeassistant.components.modbus.const import CONF_HUB, DEFAULT_HUB, MODBUS_DOMAIN
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


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Flexit Platform."""
    modbus_slave = config.get(CONF_SLAVE)
    name = config.get(CONF_NAME)
    hub = hass.data[MODBUS_DOMAIN][config.get(CONF_HUB)]
    add_entities([SystemAir(hub, modbus_slave, name)], True)


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

    def __init__(self, hub, modbus_slave, name):
        """Initialize the unit."""
        self._hub = hub
        self._name = name
        self._slave = modbus_slave

        self._fan_modes = ["Off", "Low", "Normal", "High"]

        self._input_regs = REGMAP_INPUT
        self._holding_regs = REGMAP_HOLDING
        self._current_operation = None
        self._setpoint_temp_max = None
        self._setpoint_temp_min = None
        self._current_humidity = None
        self._setpoint_humidity = None
        self._supply_temp = None
        self._extract_temp = None
        self._outdoor_temp = None
        self._user_mode = None
        self._heater = None
        self._heater_state = None
        self._filter_warning = None
        self._filter_hours = None
        self._thermal_exchange_heat_enabled = None
        self._thermal_exchange_heat_state = None
        self._thermal_exchange_cold_enabled = None
        self._thermal_exchange_cold_state = None
        self._fan_speed_supply = None
        self._fan_speed_extract = None
        # self._update_on_read = update_on_read
        self._fan_can_turn_off = None
        _LOGGER.warning("SAVE VTR COMPONENT SETUP")

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    def update(self):
        """
        Updates all of the input and holding regs dict values.
        """
        ret = True
        try:
            for k in self._input_regs:
                self._input_regs[k]["value"] = self._hub.read_input_registers(
                    unit=self._slave, address=self._input_regs[k]["addr"], count=1
                ).registers
            for k in self._holding_regs:
                self._holding_regs[k]["value"] = self._hub.read_holding_registers(
                    unit=self._slave, address=self._holding_regs[k]["addr"], count=1
                ).registers
        except AttributeError:
            # The unit does not reply reliably
            ret = False
            print("Modbus read failed")

        # self._target_temperature_max = (
        #     self._holding_regs["REG_TC_CASCADE_SP_MAX"]["value"][0] / 10.0
        # )
        # self._target_temperature_min = (
        #     self._holding_regs["REG_TC_CASCADE_SP_MIN"]["value"][0] / 10.0
        # )
        # self._current_humidity = self._holding_regs["REG_SENSOR_RHS_PDM"]["value"][0]
        # self._setpoint_humidity = self._holding_regs[
        #     "REG_ROTOR_RH_TRANSFER_CTRL_SETPOINT"
        # ]["value"][0]
        # self._supply_temp = self._holding_regs["REG_SENSOR_SAT"]["value"][0] / 10.0
        # self._extract_temp = (
        #     self._holding_regs["REG_SENSOR_PDM_EAT_VALUE"]["value"][0] / 10.0
        # )
        # self._outdoor_temp = (
        #     self.get_twos_comp(self._holding_regs["REG_SENSOR_OAT"]["value"][0]) / 10.0
        # )
        # self._user_mode = self.get_user_mode_switch(
        #     self._input_regs["REG_USERMODE_MODE"]["value"][0]
        # )
        # self._filter_warning = bool(
        #     self._input_regs["REG_FILTER_ALARM_WAS_DETECTED"]["value"][0]
        # )
        # self._filter_remaining_hours = (
        #     self._input_regs["REG_FILTER_REMAINING_TIME_L"]["value"][0] / 60 / 60
        # )
        # self._heater = bool(self._input_regs["REG_OUTPUT_Y1_DIGITAL"]["value"][0])
        # self._heater_state = self._input_regs["REG_OUTPUT_Y1_ANALOG"]["value"][0]
        # self._heat_exchanger = bool(
        #     self._input_regs["REG_OUTPUT_Y2_DIGITAL"]["value"][0]
        # )
        # self._heat_exchanger_state = self._input_regs["REG_OUTPUT_Y2_ANALOG"]["value"][
        #     0
        # ]
        # self._cooler = bool(self._input_regs["REG_OUTPUT_Y3_DIGITAL"]["value"][0])
        # self._cooler_state = self._input_regs["REG_OUTPUT_Y3_ANALOG"]["value"][0]
        # self._fan_speed_supply = self._holding_regs[
        #     "REG_USERMODE_MANUAL_AIRFLOW_LEVEL_SAF"
        # ]["value"][0]
        # self._fan_speed_extract = self._holding_regs[
        #     "REG_USERMODE_MANUAL_AIRFLOW_LEVEL_EAF"
        # ]["value"][0]
        # self._fan_can_turn_off = self._holding_regs[
        #     "REG_ROTOR_RH_TRANSFER_CTRL_SETPOINT"
        # ]["value"][0]

        return ret

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
        return self._fan_modes[self._holding_regs["fan_mode"]["value"][0] - 1]

    @property
    def fan_modes(self):
        """Return the list of available fan modes."""
        return self._fan_modes

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._input_regs["target_temperature"]["value"][0] / 10.0

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._holding_regs["supply_air_temperature"]["value"][0] / 10

    @property
    def current_humidity(self):
        """Return the temperature we try to reach."""
        return self._holding_regs["humidity"]["value"][0]

    @property
    def target_humidity(self):
        """Return the temperature we try to reach."""
        return self._holding_regs["target_humidity"]["value"][0]

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        if kwargs.get(ATTR_TEMPERATURE) is not None:
            target_temperature = kwargs.get(ATTR_TEMPERATURE, 20)
        self._hub.write_register(
            unit=self._slave,
            address=(self._holding_regs["target_temperature"]["addr"]),
            value=round(target_temperature * 10.0),
        )

    def set_fan_mode(self, fan_mode):
        """Set new fan mode."""
        fan_value = self._fan_modes.index(fan_mode) + 1

        self._hub.write_register(
            unit=self._slave,
            address=(self._holding_regs["fan_mode"]["addr"]),
            value=fan_value,
        )

    # def get_raw_input_register(self, name):
    #     """Get raw register value by name."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._input_regs[name]

    # def get_raw_holding_register(self, name):
    #     """Get raw register value by name."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._holding_regs[name]

    # def set_raw_holding_register(self, name, value):
    #     """Write to register by name."""
    #     self._hub.write_register(
    #         unit=self._slave, address=(self._holding_regs[name]["addr"]), value=value
    #     )

    # def set_fan_speed_supply(self, fan):
    #     """Set fan speed supply."""
    #     self._hub.write_register(
    #         unit=self._slave,
    #         address=(
    #             self._holding_regs["REG_USERMODE_MANUAL_AIRFLOW_LEVEL_SAF"]["addr"]
    #         ),
    #         value=fan,
    #     )

    # @property
    # def get_fan_speed_supply(self):
    #     """Get fan speed supply."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._fan_speed_supply

    # def set_fan_speed_extract(self, fan):
    #     """Set fan speed extract."""
    #     self._hub.write_register(
    #         unit=self._slave,
    #         address=(
    #             self._holding_regs["REG_USERMODE_MANUAL_AIRFLOW_LEVEL_EAF"]["addr"]
    #         ),
    #         value=fan,
    #     )

    # @property
    # def get_fan_speed_extract(self):
    #     """Get fan speed extract."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._fan_speed_extract

    # @property
    # def get_supply_temp(self):
    #     """Get supply temperature."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._supply_temp

    # def set_setpoint_temp(self, temp):
    #     self._hub.write_register(
    #         unit=self._slave,
    #         address=(self._holding_regs["REG_TC_SP"]["addr"]),
    #         value=round(temp * 10.0),
    #     )

    # @property
    # def get_setpoint_temp(self):
    #     """Get setpoint temperature."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._setpoint_temp

    # def set_setpoint_temp_max(self, temp):
    #     self._hub.write_register(
    #         unit=self._slave,
    #         address=(self._holding_regs["REG_TC_CASCADE_SP_MAX"]["addr"]),
    #         value=round(temp * 10.0),
    #     )

    # @property
    # def get_setpoint_temp_max(self):
    #     """Get setpoint temperature max."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._setpoint_temp_max

    # def set_setpoint_temp_min(self, temp):
    #     self._hub.write_register(
    #         unit=self._slave,
    #         address=(self._holding_regs["REG_TC_CASCADE_SP_MIN"]["addr"]),
    #         value=round(temp * 10.0),
    #     )

    # @property
    # def get_setpoint_temp_min(self):
    #     """Get setpoint temperature min."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._setpoint_temp_min

    # @property
    # def get_current_humidity(self):
    #     """Get  current humidity."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._current_humidity

    # def set_setpoint_humidity(self, rhs):
    #     self._hub.write_register(
    #         unit=self._slave,
    #         address=(self._holding_regs["REG_ROTOR_RH_TRANSFER_CTRL_SETPOINT"]["addr"]),
    #         value=int(rhs),
    #     )

    # @property
    # def get_setpoint_humidity(self):
    #     """Get setpoint temperature."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._setpoint_humidity

    # @property
    # def get_user_mode(self):
    #     """Get the set user mode."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._user_mode

    # @property
    # def get_extract_temp(self):
    #     """Get the extract temperature."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._extract_temp

    # @property
    # def get_outdoor_temp(self):
    #     """Get the extract temperature."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._outdoor_temp

    # @property
    # def get_filter_warning(self):
    #     """If filter warning has been generated."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._filter_warning

    # @property
    # def get_filter_remaining_hours(self):
    #     """Return remaining filter hours."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._filter_remaining_hours

    # @property
    # def get_heater(self):
    #     """Is heater active."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._heater

    # @property
    # def get_heater_state(self):
    #     """Return heater state."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._heater_state

    # @property
    # def get_heat_exchanger(self):
    #     """Is heat exchanger active."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._heat_exchanger

    # @property
    # def get_heat_exchanger_state(self):
    #     """Return heat exchanger state."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._heat_exchanger_state

    # @property
    # def get_cooler(self):
    #     """Is cooler active."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._cooler

    # @property
    # def get_cooler_state(self):
    #     """Return cooler state."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._cooler_state

    # @property
    # def get_fan_can_turn_off(self):
    #     """Return if fan can be turned off."""
    #     if self._update_on_read:
    #         self.update()
    #     return self._fan_can_turn_off


# class Flexit(ClimateEntity):
#     """Representation of a Flexit AC unit."""

#     def __init__(self, hub, modbus_slave, name):
#         """Initialize the unit."""
#         self._hub = hub
#         self._name = name
#         self._slave = modbus_slave
#         self._target_temperature = None
#         self._current_temperature = None
#         self._current_fan_mode = None
#         self._current_operation = None
#         self._fan_modes = ["Off", "Low", "Medium", "High"]
#         self._current_operation = None
#         self._filter_hours = None
#         self._filter_alarm = None
#         self._heat_recovery = None
#         self._heater_enabled = False
#         self._heating = None
#         self._cooling = None
#         self._alarm = False
#         self.unit = pyflexit(hub, modbus_slave)

#     @property
#     def supported_features(self):
#         """Return the list of supported features."""
#         return SUPPORT_FLAGS

#     def update(self):
#         """Update unit attributes."""
#         if not self.unit.update():
#             _LOGGER.warning("Modbus read failed")

#         self._target_temperature = self.unit.get_target_temp
#         self._current_temperature = self.unit.get_temp
#         self._current_fan_mode = self._fan_modes[self.unit.get_fan_speed]
#         self._filter_hours = self.unit.get_filter_hours
#         # Mechanical heat recovery, 0-100%
#         self._heat_recovery = self.unit.get_heat_recovery
#         # Heater active 0-100%
#         self._heating = self.unit.get_heating
#         # Cooling active 0-100%
#         self._cooling = self.unit.get_cooling
#         # Filter alarm 0/1
#         self._filter_alarm = self.unit.get_filter_alarm
#         # Heater enabled or not. Does not mean it's necessarily heating
#         self._heater_enabled = self.unit.get_heater_enabled
#         # Current operation mode
#         self._current_operation = self.unit.get_operation

#     @property
#     def device_state_attributes(self):
#         """Return device specific state attributes."""
#         return {
#             "filter_hours": self._filter_hours,
#             "filter_alarm": self._filter_alarm,
#             "heat_recovery": self._heat_recovery,
#             "heating": self._heating,
#             "heater_enabled": self._heater_enabled,
#             "cooling": self._cooling,
#         }

#     @property
#     def should_poll(self):
#         """Return the polling state."""
#         return True

#     @property
#     def name(self):
#         """Return the name of the climate device."""
#         return self._name

#     @property
#     def temperature_unit(self):
#         """Return the unit of measurement."""
#         return TEMP_CELSIUS

#     @property
#     def current_temperature(self):
#         """Return the current temperature."""
#         return self._current_temperature

#     @property
#     def target_temperature(self):
#         """Return the temperature we try to reach."""
#         return self._target_temperature

#     @property
#     def hvac_mode(self):
#         """Return current operation ie. heat, cool, idle."""
#         return self._current_operation

#     @property
#     def hvac_modes(self) -> List[str]:
#         """Return the list of available hvac operation modes.

#         Need to be a subset of HVAC_MODES.
#         """
#         return [HVAC_MODE_COOL]

#     @property
#     def fan_mode(self):
#         """Return the fan setting."""
#         return self._current_fan_mode

#     @property
#     def fan_modes(self):
#         """Return the list of available fan modes."""
#         return self._fan_modes

#     def set_temperature(self, **kwargs):
#         """Set new target temperature."""
#         if kwargs.get(ATTR_TEMPERATURE) is not None:
#             self._target_temperature = kwargs.get(ATTR_TEMPERATURE)
#         self.unit.set_temp(self._target_temperature)

#     def set_fan_mode(self, fan_mode):
#         """Set new fan mode."""
#         self.unit.set_fan_speed(self._fan_modes.index(fan_mode))
