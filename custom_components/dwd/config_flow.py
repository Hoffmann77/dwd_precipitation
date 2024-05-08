"""Config flow for Enphase gateway integration."""

from __future__ import annotations

import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector
from homeassistant.const import CONF_NAME

from .const import (
    DOMAIN,
    CONF_COORDINATES,
)


_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the Heat pump coordinator."""

    VERSION = 1
    MINOR_VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        pass

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the user step.

        Allows the user to specify a name and the coordinates of the location.

        """
        errors: dict[str, str] = {}
        placeholders: dict[str, str] = {}

        if user_input is not None:
            data = user_input

            if not data[CONF_NAME].lstrip(" "):
                errors["base"] = "name_invalid"

            if not errors:
                return self.async_create_entry(
                    title=data[CONF_NAME],
                    data=data,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=self.get_shema_user_step(user_input),
            description_placeholders=placeholders,
            errors=errors,
        )

    @callback
    def get_shema_user_step(self) -> vol.Schema:
        """Return the schema for the user step."""
        schema = {
            vol.Required(CONF_NAME): str,
            vol.Required(CONF_COORDINATES): selector.LocationSelector(
                selector.LocationSelectorConfig()
            ),
        }

        return vol.Schema(schema)
