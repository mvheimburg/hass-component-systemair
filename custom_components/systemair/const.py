"""Constants for the systemair integration."""

# import datetime
# import timedelta
from typing import Final
from pysystemair import const as sysconst

from homeassistant.components.climate.const import (
    FAN_AUTO,
    FAN_OFF,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_HIGH,
    HVAC_MODE_COOL,
    HVAC_MODE_DRY,
    HVAC_MODE_FAN_ONLY,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    SUPPORT_FAN_MODE,
    SUPPORT_TARGET_TEMPERATURE,
)


SLAVE_ADRESS = "slave address"
UNIT_NAME = "unit name (for HA)"
DOMAIN: Final = "systemair"

DEFAULT_TEMPERATURE = 20


HASS_TO_SYSTEMAIR_FAN_MODES = {
    FAN_OFF: sysconst.FAN_MODES.OFF,
    FAN_LOW: sysconst.FAN_MODES.LOW,
    FAN_MEDIUM: sysconst.FAN_MODES.NORMAL,
    FAN_HIGH: sysconst.FAN_MODES.HIGH,
}
SYSTEMAIR_TO_HASS_FAN_MODES = {
    sysconst.FAN_MODES.OFF: FAN_OFF,
    sysconst.FAN_MODES.LOW: FAN_LOW ,
    sysconst.FAN_MODES.NORMAL: FAN_MEDIUM,
    sysconst.FAN_MODES.HIGH: FAN_HIGH,
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


USER_MODES = list(sysconst.USER_MODES.values())

ATTR_HUMIDITY: Final = "humidity"



