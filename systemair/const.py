"""Constants for the systemair integration."""

# import datetime
# import timedelta

from homeassistant.components.climate.const import (
    FAN_AUTO,
    FAN_HIGH,
    FAN_LOW,
    FAN_MEDIUM,
    HVAC_MODE_COOL,
    HVAC_MODE_DRY,
    HVAC_MODE_FAN_ONLY,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    SUPPORT_FAN_MODE,
    SUPPORT_TARGET_TEMPERATURE,
)

# DOMAIN = "systemair"
DEVICE_DEFAULT_NAME = "SystemAir"
SAVE_VTR = "save_vtr"

REGMAP_INPUT = {
    "target_temperature": {
        "addr": 2053,
        "value": 0,
    },  # REG_TC_SP_SATC: Temperature setpoint for the supply air temperature
    "REG_FILTER_REMAINING_TIME_L": {
        "addr": 7004,
        "value": 0,
    },  # REG_FILTER_REMAINING_TIME_L: Remaining filter time in seconds, lower 16 bits
    "REG_OUTPUT_Y3_ANALOG": {
        "addr": 14200,
        "value": 0,
    },  # REG_OUTPUT_Y3_ANALOG: Cooler AO state
    "REG_OUTPUT_Y3_DIGITAL": {
        "addr": 14201,
        "value": 0,
    },  # REG_OUTPUT_Y3_DIGITAL: Cooler DO state:0: Output not active1: Output active
    "REG_OUTPUT_Y2_ANALOG": {
        "addr": 14102,
        "value": 0,
    },  # REG_OUTPUT_Y2_ANALOG: Heat Exchanger AO state.
    "REG_OUTPUT_Y2_DIGITAL": {
        "addr": 14101,
        "value": 0,
    },  # REG_OUTPUT_Y2_DIGITAL: Heat Exchanger DO state.0: Output not active1: Output active
    "REG_OUTPUT_Y1_ANALOG": {
        "addr": 14100,
        "value": 0,
    },  # REG_OUTPUT_Y1_ANALOG: Heater AO state.
    "REG_OUTPUT_Y1_DIGITAL": {
        "addr": 14101,
        "value": 0,
    },  # REG_OUTPUT_Y1_DIGITAL: Heater DO state:0: Output not active1: Output active
    "REG_FILTER_ALARM_WAS_DETECTED": {
        "addr": 7006,
        "value": 0,
    },  # REG_FILTER_ALARM_WAS_DETECTED: Indicates if the filter warning alarm was generated.
    "REG_USERMODE_MODE": {
        "addr": 1160,
        "value": 0,
    },  # REG_USERMODE_MODE: Active User mode.0: Auto1: Manual2: Crowded3: Refresh4: Fireplace5: Away6: Holiday7: Cooker Hood8: Vacuum Cleaner9: CDI110: CDI211: CDI312: PressureGuard
    "REG_SPEED_SAF_DESIRED_OFF": {
        "addr": 1351,
        "value": 0,
    },  # REG_SPEED_SAF_DESIRED_OFF: Indicates that the SAF shall be turned off once the electrical reheater is cooled down
}

REGMAP_HOLDING = {
    "target_temperature": {
        "addr": 2000,
        "value": 0,
    },  # REG_TC_SP: Temperature setpoint for the supply air temperature
    "supply_air_temperature": {
        "addr": 12102,
        "value": 0,
    },  # REG_SENSOR_SAT: Supply Air Temperature sensor (standard)
    "outdoor_air_temperature": {
        "addr": 12100,
        "value": 0,
    },  # REG_SENSOR_OAT: Outdoor Air Temperature sensor (standard)
    "fan_mode": {
        "addr": 1130,
        "value": 0,
    },  # REG_USERMODE_MANUAL_AIRFLOW_LEVEL_SAF:  Fan speed level for mode Manual, supply fan.(1): value Off only allowed if contents of register 1352 is 1: Off 2: Low 3: Normal 4:High
    "REG_USERMODE_MANUAL_AIRFLOW_LEVEL_EAF": {
        "addr": 1131,
        "value": 0,
    },  # Fan speed level for mode Manual, extract fan. 2: Low 3: Normal 4: High
    "humidity": {
        "addr": 12135,
        "value": 0,
    },  # REG_SENSOR_RHS_PDM: PDM RHS sensor value (standard)
    "REG_SENSOR_PDM_EAT_VALUE": {
        "addr": 12543,
        "value": 0,
    },  # PDM EAT sensor value (standard)
    "REG_TC_CASCADE_SP_MIN": {
        "addr": 2020,
        "value": 0,
    },  # Minimum temperature set point for the SATC
    "REG_TC_CASCADE_SP_MAX": {
        "addr": 2021,
        "value": 0,
    },  # Maximum temperature set point for the SATC
    "target_humidity": {
        "addr": 2202,
        "value": 0,
    },  # REG_ROTOR_RH_TRANSFER_CTRL_SETPOINT: Set point setting for RH transfer control
}

HVAC_MODES = [
    HVAC_MODE_OFF,
    HVAC_MODE_COOL,
    HVAC_MODE_HEAT,
    HVAC_MODE_FAN_ONLY,
    HVAC_MODE_DRY,
]

SA_FAN_MODE_OFF = "off"
SA_FAN_MODE_LOW = "low"
SA_FAN_MODE_MEDIUM = "medium"
SA_FAN_MODE_HIGH = "high"

FAN_MODE = {
    1: SA_FAN_MODE_OFF,
    2: SA_FAN_MODE_LOW,
    3: SA_FAN_MODE_MEDIUM,
    4: SA_FAN_MODE_HIGH,
}

SA_OPERATION_MODE_AUTO = "auto"
SA_OPERATION_MODE_MANUAL = "manual"
SA_OPERATION_MODE_CROWDED = "crowded"
SA_OPERATION_MODE_REFRESH = "refresh"
SA_OPERATION_MODE_FIREPLACE = "fireplace"
SA_OPERATION_MODE_HOLIDAY = "holiday"
SA_OPERATION_MODE_IDLE = "idle"

# Custom
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

# POSTPROCESS_NO = lambda x: x
# POSTPROCESS_TEMPERATURE = lambda x: x / 10.0
# POSTPROCESS_DAYS_UNTIL = lambda x: (
#     (datetime.now() + timedelta(seconds=x)) - datetime.today()
# ).days
# POSTPROCESS_OPERATION = lambda x: USER_MODE[int(x)]
# POSTPROCESS_FAN_MODE = lambda x: FAN_MODE[int(x)]
# POSTPROCESS_ALARM = lambda x: ALARM_MODES[str(x)]

# # Postprocessing
# POSTPROCESS_MAP = {
#     SENSOR_CURRENT_FAN_MODE: POSTPROCESS_FAN_MODE,
#     SENSOR_TEMPERATURE_OUTDOOR: POSTPROCESS_TEMPERATURE,
#     SENSOR_TEMPERATURE_SUPPLY: POSTPROCESS_TEMPERATURE,
#     SENSOR_TEMPERATURE_EXTRACT: POSTPROCESS_TEMPERATURE,
#     SENSOR_FILTER_TIME: POSTPROCESS_DAYS_UNTIL,
#     SENSOR_CURRENT_OPERATION: POSTPROCESS_OPERATION,
#     SENSOR_TARGET_TEMPERATURE: POSTPROCESS_TEMPERATURE,
#     SENSOR_ALARM_FROST_PROTECTION: POSTPROCESS_ALARM,
#     SENSOR_ALARM_FROST_PROTECTION_SENSOR: POSTPROCESS_ALARM,
#     SENSOR_ALARM_DEFROST: POSTPROCESS_ALARM,
#     SENSOR_ALARM_SUPPLY_RPM: POSTPROCESS_ALARM,
#     SENSOR_ALARM_EXTRACT_RPM: POSTPROCESS_ALARM,
#     SENSOR_ALARM_SUPPLY_FLOW_PRESSURE: POSTPROCESS_ALARM,
#     SENSOR_ALARM_EXTRACT_FLOW_PRESSURE: POSTPROCESS_ALARM,
#     SENSOR_ALARM_ELECTRICAL_HEATER: POSTPROCESS_ALARM,
#     SENSOR_ALARM_BYPASS_DAMPER: POSTPROCESS_ALARM,
#     SENSOR_ALARM_ROTARY_EXCHANGER: POSTPROCESS_ALARM,
#     SENSOR_ALARM_BYPASS_DAMPER_2: POSTPROCESS_ALARM,
#     SENSOR_ALARM_OUTDOOR_TEMP_SENSOR: POSTPROCESS_ALARM,
#     SENSOR_ALARM_REHEATER_TEMP_SENSOR: POSTPROCESS_ALARM,
#     SENSOR_ALARM_SUPPLY_TEMP_SENSOR: POSTPROCESS_ALARM,
#     SENSOR_ALARM_INDOOR_TEMP_SENSOR: POSTPROCESS_ALARM,
#     SENSOR_ALARM_EXTRACT_TEMP_SENSOR: POSTPROCESS_ALARM,
#     SENSOR_ALARM_PREHEATER_TEMP_SENSOR: POSTPROCESS_ALARM,
#     SENSOR_ALARM_EFFICIENCY_TEMP_SENSOR: POSTPROCESS_ALARM,
#     SENSOR_ALARM_PDM_RH: POSTPROCESS_ALARM,
#     SENSOR_ALARM_PDM_TEMP: POSTPROCESS_ALARM,
#     SENSOR_ALARM_CHANGE_FILTER: POSTPROCESS_ALARM,
#     SENSOR_ALARM_EXTRA_CONTROLLER: POSTPROCESS_ALARM,
#     SENSOR_ALARM_EXTERNAL_STOP: POSTPROCESS_ALARM,
#     SENSOR_ALARM_MANUAL_STOP: POSTPROCESS_ALARM,
#     SENSOR_ALARM_REHEATER_OVERHEAT: POSTPROCESS_ALARM,
#     SENSOR_ALARM_SUPPLY_TEMP_LOW: POSTPROCESS_ALARM,
#     SENSOR_ALARM_CO2: POSTPROCESS_ALARM,
#     SENSOR_ALARM_RH: POSTPROCESS_ALARM,
#     SENSOR_ALARM_INCORRECT_MANUAL_MODE: POSTPROCESS_ALARM,
# }