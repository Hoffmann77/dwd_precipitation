"""Home assistant base entities."""

from __future__ import annotations

from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo

from .const import DOMAIN
from .coordinator import DwdUpdateCoordinator


class DwdCoordinatorEntity(CoordinatorEntity[DwdUpdateCoordinator]):
    """Coordinator entity."""

    entity_description: EntityDescription
    _attr_has_entity_name = True

    def __init__(
            self,
            coordinator: DwdUpdateCoordinator,
            description: EntityDescription,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)

        self.entity_description = description
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name=coordinator.config_entry.title or "Heat pump Signal",
        )
