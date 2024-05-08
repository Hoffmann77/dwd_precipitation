"""Module for custom home-assistant exceptions."""

import httpx

from homeassistant.exceptions import HomeAssistantError


def create_hass_exception(input_exception):
    """Create a hass exception."""
    name = input_exception.__class__.__name__
    return type(name, (HomeAssistantError,))


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

    pass


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""

    pass


class EnlightenInvalidAuth(HomeAssistantError):
    """Error to indicate invalid auth to Enlighten.

    Raises when status 401 is raised while trying to login to enlighten.
    """

    pass


class InvalidToken(HomeAssistantError):
    """Error to indicate an invalid token.

    Raises if the token provided by the user is invalid.
    """

    pass


class TokenConfigurationError(ValueError):
    """Error for invalid combination of arguments in EnphaseToken.

    Raised when the provided combination of arguments in EnphaseToken is
    not supported.

    """

    pass


class InvalidEnphaseToken(ValueError):
    """Error for invalid Enphase tokens.

    Is raised if token validation using /auth/check_jwt returns
    invalid as response.

    """

    pass


class EnlightenUnauthorized(httpx.HTTPStatusError):
    """Error for invalid Enlighten credentials.

    Is raised if status 401 is returned while trying to login to enlighten.

    """

    pass
