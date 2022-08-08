"""The SystemAir integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

PLATFORMS = [Platform.CLIMATE]

from .const import (
    DOMAIN,
    SERVICE_SET_COTWO_MEAS,
    ATTR_CO2_PPM
)

# async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
#     """Set up climate entities."""
#     component = hass.data[DOMAIN] = EntityComponent(
#         _LOGGER, DOMAIN, hass, SCAN_INTERVAL
#     )

#     component.async_register_entity_service(
#         SERVICE_SET_COTWO_MEAS,
#         {
#             vol.Required('value'): int,
#         },
#         "async_set_cotwo_meas",
#     )


#     return True

# SET_COTWO_MEAS_SCHEMA=vol.Schema({
#                             # vol.Required(ATTR_ENTITY_ID): cv.entity_id,
#                             vol.Required(ATTR_VALUE): int,
#                         })


# async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
#     """Set up climate entities."""
#     hass.data[DOMAIN] = {}

#     component.async_register_entity_service(
#         SERVICE_SET_COTWO_MEAS, 
#         SET_COTWO_MEAS_SCHEMA, 
#         f"async_{SERVICE_SET_COTWO_MEAS}")
#     # component.async_register_entity_service(SERVICE_TURN_OFF, {}, "async_turn_off")
  
#     # component.async_register_entity_service(
#     #     SERVICE_SET_SWING_MODE,
#     #     {vol.Required(ATTR_SWING_MODE): cv.string},
#     #     "async_set_swing_mode",
#     #     [ClimateEntityFeature.SWING_MODE],
#     # )

#     return True



async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SystemAir from a config flow."""
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    
    # platform = entity_platform.async_get_current_platform()

    # # This will call Entity.set_sleep_timer(sleep_time=VALUE)
    # platform.async_register_entity_service(
    #     SERVICE_SET_COTWO,
    #     {
    #         vol.Required('value'): cv.int,
    #     },
    #     "set_cotwo",
    # )
    
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old entry."""
    # convert title and unique_id to string
    if config_entry.version == 1:
        if isinstance(config_entry.unique_id, int):

            hass.config_entries.async_update_entry(
                config_entry,
                unique_id=str(config_entry.unique_id),
                title=str(config_entry.title),
            )

    return True



# async def async_set_cotwo_meas(
#     entity: SystemAir, service_call: ServiceCall
# ) -> None:
#     """Handle aux heat service."""
#     if service_call.data[SERVICE_SET_COTWO_MEAS]:
#         value=service_call.data[ATTR_VALUE]
#         _LOGGER.warning(value)
#         await entity.async_set_cotwo_meas(value)
#     else:
#         _LOGGER.warning("UNKNOWN SERVICE")


# async def set_cotwo(entity, service_call):
#     await entity.set_cotwo(service_call.data['value'])