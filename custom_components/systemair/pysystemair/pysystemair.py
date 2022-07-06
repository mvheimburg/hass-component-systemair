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
        self._registers = RegMap


    async def async_update_all(self):
        """
        Updates all of the input and holding regs dict values.
        """
       
        for key, register in self._registers.items():
            # _LOGGER.warning(f"Updating register for {key} {register}")
            # _LOGGER.warning(f"register.addr == {register.addr}")
            # _LOGGER.warning(f"register.reg_type == {register.reg_type}")
            try:
                await self.async_update_from_register(key, register)
                # result=None
                # if register.reg_type == REG_TYPE.INPUT:
                #     result = await self._async_callback_input_reg(address=register.addr)
                # elif register.reg_type == REG_TYPE.HOLDING:
                #     result = await self._async_callback_holding_reg(address=register.addr)
                # else:
                #     _LOGGER.warning(f"register.reg_type not matched")
                # # _LOGGER.warning(f"result= {result}")
                # if result is None:
                #     _LOGGER.warning(f"Error reading {variable} value from SystemAir modbus adapter")
                # else:
                #     register.value = result.registers[0]
            except AttributeError:
                 _LOGGER.warning(f"Modbus read failed for {key}")

    async def async_update_from_register(self, key, register):
        """
        Updates all of the input and holding regs dict values.
        """
        try:
            result=None
            _LOGGER.warning(f"register.addr == {register.addr}")
            _LOGGER.warning(f"register.reg_type == {register.reg_type}")
            if register.reg_type == REG_TYPE.INPUT:
                _LOGGER.warning(f"calling {self._async_callback_input_reg}")
                result = await self._async_callback_input_reg(address=register.addr)
            elif register.reg_type == REG_TYPE.HOLDING:
                _LOGGER.warning(f"calling {self._async_callback_holding_reg}")
                result = await self._async_callback_holding_reg(address=register.addr)

            if result is None:
                 _LOGGER.warning(f"Error reading {key} value from SystemAir modbus adapter")
            else:
                _LOGGER.warning(f"{key} value is {result.registers[0]}")
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

    # @property
    # def user_modes(self):
    #     """Return the fan setting."""
    #     return list( USER_MODES.values())




    @property
    def fan_mode(self):
        """Return the fan setting."""
        if self._registers.saf_usermode_fs.value is None:
            return 3
        return self._registers.saf_usermode_fs.value



    @property
    def filter_hours(self):
        if self._registers.remaining_filter_time_.value is None:
            return 0
        return self._registers.remaining_filter_time_.value 

    @property
    def filter_alarm(self):
        if self._registers.filter_alarm_.value is None:
            return 0
        return self._registers.filter_alarm_.value

    @property
    def heat_exchanger_active(self):
        if self._registers.heat_exchanger_active_.value is None:
            return 0
        return self._registers.heat_exchanger_active_.value
    
    @property
    def heat_exchanger(self):
        if self._registers.heat_exchanger_.value is None:
            return 0
        return self._registers.heat_exchanger_.value

 
    # @property
    # def heating(self):
    #     if self._registers.oa_temperature_sensor.value is None:
    #         return 0
    #     return self._registers.oa_temperature_sensor.value / 10.0


    @property
    def heater_enabled(self):
        if self._registers.heater_active_.value is None:
            return 0
        return self._registers.heater_active_.value

    # @property
    # def cooling_enabled(self):  
    #     if self._registers.oa_temperature_sensor.value is None:
    #         return 0
    #     return self._registers.oa_temperature_sensor.value / 10.0


    @property
    def free_cooling_enabled(self): 
        if self._registers.free_cooling_enabled.value is None:
            return 0
        return self._registers.free_cooling_enabled.value


    @property
    def free_cooling_active(self):
        if self._registers.free_cooling_active.value is None:
            return 0
        return self._registers.free_cooling_active.value


    @property
    def free_cooling_start_time(self):
        if self._registers.free_cooling_start_time_h.value is None or self._registers.free_cooling_start_time_m.value is None:
            return 0
        return f"{self._registers.free_cooling_start_time_h.value}:{self._registers.free_cooling_start_time_m.value}"

    @property
    def free_cooling_end_time(self): 
        if self._registers.free_cooling_end_time_h.value is None or self._registers.free_cooling_end_time_m.value is None:
            return 0
        return f"{self._registers.free_cooling_end_time_h.value}:{self._registers.free_cooling_end_time_m.value}"

    @property
    def outdoor_air_temp(self):
        if self._registers.oa_temperature_sensor.value is None:
            return 0
        return self._registers.oa_temperature_sensor.value / 10.0


    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        if self._registers.target_temperature.value is None:
            return 0
        return self._registers.target_temperature.value / 10.0

    @property
    def current_temperature(self):
        """Return the current temperature."""
        if self._registers.sa_temperature_sensor.value is None:
            return 0
        return self._registers.sa_temperature_sensor.value / 10

    @property
    def current_humidity(self):
        """Return the temperature we try to reach."""
        if self._registers.pdm_humidity_sensor.value is None:
            return 0
        return self._registers.pdm_humidity_sensor.value

    @property
    def target_humidity(self):
        """Return the temperature we try to reach."""
        if self._registers.target_humidity.value is None:
            return 0
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
        
