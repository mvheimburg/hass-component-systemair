from typing import Awaitable, Callable
import logging
_LOGGER = logging.getLogger(__name__)
from .const import *
from .models import (
    RegMap
    ,InputRegister,HoldingRegister,Register
)
class PySystemAir():
    _async_callback_holding_reg: Awaitable
    _async_callback_input_reg: Awaitable
    _async_callback_write_reg: Awaitable

    def __init__(self, async_callback_holding_reg=None, async_callback_input_reg=None, async_callback_write_reg=None):
        if async_callback is None:
            #Todo, make connection and callback
            pass
        else:
            self._async_callback_holding_reg=async_callback_holding_reg
            self._async_callback_input_reg=async_callback_input_reg
            self._async_callback_write_reg=async_callback_write_reg
        # self._slave=slave
        # self._update_on_read = update_on_read
        self._registers = RegMap()


    async def async_update_all(self):
        """
        Updates all of the input and holding regs dict values.
        """
        try:
            for key, register in self._registers.dict().items():
                await self.async_update_from_register(register)
        except AttributeError:
            print(f"Modbus read failed for {key}")

    async def async_update_from_register(self, register:Register):
        """
        Updates all of the input and holding regs dict values.
        """
        try:
            result=None
            if register.reg_type == REG_TYPE.INPUT:
                result = await self._async_callback_input_reg(address=register.addr)
            elif reg_type == REG_TYPE.HOLDING:
                result = await self._async_callback_holding_reg(address=register.addr)

            if result is None:
                 _LOGGER.warning(f"Error reading {variable} value from SystemAir modbus adapter")
            else:
                register.value = result.registers[0]
        except AttributeError as e:
            raise e


    async def async_write_to_register(self, register:Register, value):
        """
        Updates all of the input and holding regs dict values.
        """
        try:
            if await self._async_callback_write_reg(address=register.addr, value=value):
                    register.value = value
            else:
                _LOGGER.error(f"Unable to write {variable} to SystemAir modbus interface") 
        except AttributeError as e:
            raise e

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        # if self._update_on_read:
        #     await self.update_from_register("input", "target_temperature")
        return self._registers.target_temperature.value / 10.0

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._registers.sa_temperature_sensor.value / 10

    @property
    def current_humidity(self):
        """Return the temperature we try to reach."""
        return self._registers.pdm_humidity_sensor.value

    @property
    def target_humidity(self):
        """Return the temperature we try to reach."""
        # if self._update_on_read:
        #     await self.update_from_register("holding", "target_humidity")
        return self._registers.target_humidity.value

    async def async_set_temperature(self, value):
        """Set new target temperature."""
        await self.async_write_to_register(self._registers.target_temperature, value)



    async def async_set_fan_mode(self, fan_mode):
        """Set new fan mode."""
        fan_value = FAN_MODES(fan_mode)
        await self.async_write_to_register(self._registers.saf_usermode_fs, value)
        await self.async_write_to_register(self._registers.eaf_usermode_fs, value)
        # _LOGGER.warning(f"Setting fan_value: {fan_value} with type: {type(fan_value)}")
        # if await self._hub.async_pymodbus_call(
        # unit=self._slave,
        # address=(self._holding_regs["fan_mode"]["addr"]),
        # value=fan_value,
        # use_call=CALL_TYPE_WRITE_REGISTER):
        #     self._holding_regs["fan_mode"]["value"] = fan_value
        # else:
        #      _LOGGER.error("Unable to set tempereatur to SystemAir modbus interface")

    # asypass

    async def async_set_humidity(self, humidity):
        """Set new target temperature."""
    #    if kwargs.get(ATTR_HUMIDITY) is not None:
    #        target_humidity = kwargs.get(ATTR_HUMIDITY, 30)
        target_humidity=int(round(humidity))
        pass
    #     _LOGGER.warning(f"Setting humidity: {target_humidity} with type: {type(target_humidity)}")
    #     if await self._hub.async_pymodbus_call(
    #        unit=self._slave,
    #        address=(self._holding_regs["target_humidity"]["addr"]),
    #        value=target_humidity,
    #        use_call=CALL_TYPE_WRITE_REGISTER):
    #         self._holding_regs["target_humidity"]["value"] = target_humidity
    #     else:
    #          _LOGGER.error("Unable to set tempereatur to SystemAir modbus interface")nc def set_humidity(self, **kwargs):
    # #