"""The Heat pump Signal integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.httpx_client import get_async_client
from homeassistant.core import HomeAssistant

from .coordinator import DwdUpdateCoordinator
from .const import (
    DOMAIN, PLATFORMS,
)


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Enphase Gateway from a config entry."""
    coordinator = DwdUpdateCoordinator(hass, entry, get_async_client())

    await coordinator.async_config_entry_first_refresh()

    # if not entry.unique_id:
    #     hass.config_entries.async_update_entry(
    #         entry,
    #         unique_id=reader.serial_number
    #     )

    entry.async_on_unload(entry.add_update_listener(update_listener))
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle config_entry updates."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the config entries."""
    unload = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload


async def async_migrate_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
) -> bool:
    """Migrate old config entry."""
    _LOGGER.debug(
        f"Migrating config entry from version {config_entry.version}"
    )

    if config_entry.version == 0:
        data_new = {**config_entry.data}
        options_new = {}

        config_entry.version = 1
        hass.config_entries.async_update_entry(
            config_entry,
            data=data_new,
            options=options_new
        )

    _LOGGER.info("Migration to version {config_entry.version} successful")

    return True
