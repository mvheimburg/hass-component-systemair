"""Constants for the systemair integration."""

from typing import Final
from enum import IntEnum, Enum


# DOMAIN = "systemair"
DEVICE_DEFAULT_NAME = "SystemAir"
SAVE_VTR = "save_vtr"

UPDATE_ON_READ = True
DEFAULT_TEMPERATURE = 20

class REG_TYPE(IntEnum):
    INPUT=1
    HOLDING=2

class FAN_MODES(Enum):
    OFF=1
    LOW=2   
    NORMAL=3
    HIGH=4

# class REGMAP_INPUT():
#     target_temperature: {
#         "addr": 2053,
#         "value":None,
#     },  # REG_TC_SP_SATC: Temperature setpoint for the supply air temperature
#     "REG_FILTER_REMAINING_TIME_L": {
#         "addr": 7004,
#         "value":None,
#     },  # REG_FILTER_REMAINING_TIME_L: Remaining filter time in seconds, lower 16 bits
#     "REG_OUTPUT_Y3_ANALOG": {
#         "addr": 14200,
#         "value":None,
#     },  # REG_OUTPUT_Y3_ANALOG: Cooler AO state
#     "REG_OUTPUT_Y3_DIGITAL": {
#         "addr": 14201,
#         "value":None,
#     },  # REG_OUTPUT_Y3_DIGITAL: Cooler DO state:0: Output not active1: Output active
#     "REG_OUTPUT_Y2_ANALOG": {
#         "addr": 14102,
#         "value":None,
#     },  # REG_OUTPUT_Y2_ANALOG: Heat Exchanger AO state.
#     "REG_OUTPUT_Y2_DIGITAL": {
#         "addr": 14101,
#         "value":None,
#     },  # REG_OUTPUT_Y2_DIGITAL: Heat Exchanger DO state.0: Output not active1: Output active
#     "REG_OUTPUT_Y1_ANALOG": {
#         "addr": 14100,
#         "value":None,
#     },  # REG_OUTPUT_Y1_ANALOG: Heater AO state.
#     "REG_OUTPUT_Y1_DIGITAL": {
#         "addr": 14101,
#         "value":None,
#     },  # REG_OUTPUT_Y1_DIGITAL: Heater DO state:0: Output not active1: Output active
#     "REG_FILTER_ALARM_WAS_DETECTED": {
#         "addr": 7006,
#         "value":None,
#     },  # REG_FILTER_ALARM_WAS_DETECTED: Indicates if the filter warning alarm was generated.
#     "REG_USERMODE_MODE": {
#         "addr": 1160,
#         "value":None,
#     },  # REG_USERMODE_MODE: Active User mode.0: Auto1: Manual2: Crowded3: Refresh4: Fireplace5: Away6: Holiday7: Cooker Hood8: Vacuum Cleaner9: CDI110: CDI211: CDI312: PressureGuard
#     "REG_SPEED_SAF_DESIRED_OFF": {
#         "addr": 1351,
#         "value":None,
#     },  # REG_SPEED_SAF_DESIRED_OFF: Indicates that the SAF shall be turned off once the electrical reheater is cooled down
# }

# REGMAP_HOLDING = {
#     "target_temperature": {
#         "addr": 2000,
#         "value":None,
#     },  # REG_TC_SP: Temperature setpoint for the supply air temperature
#     "supply_air_temperature": {
#         "addr": 12102,
#         "value":None,
#     },  # REG_SENSOR_SAT: Supply Air Temperature sensor (standard)
#     "outdoor_air_temperature": {
#         "addr": 12100,
#         "value":None,
#     },  # REG_SENSOR_OAT: Outdoor Air Temperature sensor (standard)
#     "fan_mode": {
#         "addr": 1130,
#         "value":None,
#     },  # REG_USERMODE_MANUAL_AIRFLOW_LEVEL_SAF:  Fan speed level for mode Manual, supply fan.(1): value Off only allowed if contents of register 1352 is 1: Off 2: Low 3: Normal 4:High
#     "REG_USERMODE_MANUAL_AIRFLOW_LEVEL_EAF": {
#         "addr": 1131,
#         "value":None,
#     },  # Fan speed level for mode Manual, extract fan. 2: Low 3: Normal 4: High
#     "humidity": {
#         "addr": 12135,
#         "value":None,
#     },  # REG_SENSOR_RHS_PDM: PDM RHS sensor value (standard)
#     "REG_SENSOR_PDM_EAT_VALUE": {
#         "addr": 12543,
#         "value":None,
#     },  # PDM EAT sensor value (standard)
#     "REG_TC_CASCADE_SP_MIN": {
#         "addr": 2020,
#         "value":None,
#     },  # Minimum temperature set point for the SATC
#     "REG_TC_CASCADE_SP_MAX": {
#         "addr": 2021,
#         "value":None,
#     },  # Maximum temperature set point for the SATC
#     "target_humidity": {
#         "addr": 2202,
#         "value":None,
#     }, 
#     "REG_SENSOR_CO2S": {
#         "addr": 12115,
#         "value":None,
#     }
# }

# class HVAC_MODES(Enum):
#     OFF = "off"
#     HEAT = "heat"
#     COOL = "cool"
#     AUTO = "auto"
#     DRY = "dry"
#     FAN_ONLY = "fan_only"


# SA_FAN_MODE_OFF = "off"
# SA_FAN_MODE_LOW = "low"
# SA_FAN_MODE_MEDIUM = "medium"
# SA_FAN_MODE_HIGH = "high"

# FAN_MODE = {
#     1: SA_FAN_MODE_OFF,
#     2: SA_FAN_MODE_LOW,
#     3: SA_FAN_MODE_MEDIUM,
#     4: SA_FAN_MODE_HIGH,
# }

SA_OPERATION_MODE_AUTO = "auto"
SA_OPERATION_MODE_MANUAL = "manual"
SA_OPERATION_MODE_CROWDED = "crowded"
# SA_OPERATION_MODE_REFRESH = "refresh"
# SA_OPERATION_MODE_FIREPLACE = "fireplace"
SA_OPERATION_MODE_HOLIDAY = "holiday"
SA_OPERATION_MODE_IDLE = "idle"
SA_OPERATION_MODE_OFF = "off"

USER_MODE = {
    0: SA_OPERATION_MODE_AUTO,
    1: SA_OPERATION_MODE_MANUAL,
    2: SA_OPERATION_MODE_CROWDED,
    3: SA_OPERATION_MODE_REFRESH,
    4: SA_OPERATION_MODE_FIREPLACE,
    5: SA_OPERATION_MODE_IDLE,
    6: SA_OPERATION_MODE_HOLIDAY,
}

ATTR_HUMIDITY: Final = "humidity"