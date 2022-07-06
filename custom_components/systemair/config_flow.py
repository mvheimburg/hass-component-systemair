"""Config flow for SystemAir modbus integration."""
from __future__ import annotations

import logging
from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_UNIQUE_ID,
    CONF_NAME,
    CONF_SLAVE,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import(
    UNIT_NAME,
    SLAVE_ADRESS,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

ENTRY_SCHEMA = vol.Schema(
    {
        vol.Required(UNIT_NAME, default=DOMAIN): cv.string,
        vol.Required(SLAVE_ADRESS, default=1): int
    }
)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Adax."""

    VERSION = 2

    async def async_step_user(self, user_input:Optional[Dict[str, Any]]=None) -> FlowResult:
        """Handle the initial step."""

        if user_input is not None:
            return self.async_create_entry(
                title=DOMAIN,
                data={
                    CONF_NAME: user_input[UNIT_NAME],
                    CONF_SLAVE: user_input[SLAVE_ADRESS]
                },)

        return self.async_show_form(
            step_id="user",
            data_schema=ENTRY_SCHEMA,)