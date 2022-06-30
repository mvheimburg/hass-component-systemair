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
        self._async_callback_holding_reg=async_callback_holding_reg
        self._async_callback_input_reg=async_callback_input_reg
        self._async_callback_write_reg=async_callback_write_reg
        self._registers = RegMap()


    async def async_update_all(self):
        """
        Updates all of the input and holding regs dict values.
        """
       
        for key, register in self._registers.dict().items():
            try:
                print(f"Updating register for {key}")
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
    def fan_mode(self):
        """Return the fan setting."""
        return self._registers.saf_usermode_fs.value

    @property
    def fan_modes(self):
        """Return the fan setting."""
        return self._registers.saf_usermode_fs.value

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
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
        return self._registers.target_humidity.value


    async def async_set_temperature(self, value):
        """Set new target temperature."""
        await self.async_write_to_register(self._registers.target_temperature, value)


    async def async_set_fan_mode(self, value):
        """Set new fan mode."""
        value = FAN_MODES(value)
        await self.async_write_to_register(self._registers.saf_usermode_fs, value)
        await self.async_write_to_register(self._registers.eaf_usermode_fs, value)


    async def async_set_humidity(self, value):
        """Set new target temperature."""
        target_humidity=int(round(value))
        
