"""Data update coordinator for the Heat pump signal integration."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
# from homeassistant.helpers.storage import Store
from homeassistant.const import CONF_NAME
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    # UpdateFailed,
)

from .signals import SIGNALS
from .const import CONF_COORDINATES
from .radolan import Radolan

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL = timedelta(seconds=300)


@dataclass(slots=True)
class Precipitation:
    """Model for precipitation data."""

    radolan_rw: int
    radolan_sf: int

    @classmethod
    def from_data(cls, data: dict) -> Precipitation:
        """Return instance of Precipitation."""
        return cls(
            radolan_rw=data["radolan_rw"],
            radolan_sf=data["radolan_sf"],
        )


class DwdUpdateCoordinator(DataUpdateCoordinator):
    """Data update coordinator."""

    def __init__(
            self,
            hass: HomeAssistant,
            entry: ConfigEntry,
            async_client,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=entry.data[CONF_NAME],
            update_interval=UPDATE_INTERVAL,
        )
        self.config_entry = entry
        self.async_client = async_client
        self.coords = entry.data[CONF_COORDINATES]
        self.lat = self.coords["latitude"]
        self.lon = self.coords["longitude"]
        self.products = [
            Radolan("rw", self._lat, self._lon, self.async_client),
            Radolan("rw", self._lat, self._lon, self.async_client),
        ]

    async def _async_update_data(self) -> Precipitation:
        """Update the data and the signal."""
        data = {}
        for product in self.products:
            data[product.key] = product.update()

        return Precipitation.from_data(data)
