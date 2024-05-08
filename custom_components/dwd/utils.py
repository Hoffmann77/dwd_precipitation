"""Utils module."""

from typing import Any

from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN

ERROR_STATES = {STATE_UNAVAILABLE, STATE_UNKNOWN}


def get_state_as_float(
        states: dict,
        entity_id: str,
        normalize: bool = True,
) -> float:
    """Return the state of the given entity as float.

    Parameters
    ----------
    states : dict
        Homeassistant instances states dict.
    entity_id : str
        Entity id.
    normalize : bool, optional
        Whether to normalize the value. The default is True.

    Returns
    -------
    float or str or None
        States value as float.
        Returns `unknown` or `unavailable` if the state matches ERROR_STATES.
        Return `None` if the state is not the states machine.

    """
    if not entity_id:
        return None

    state_obj = states.get(entity_id)
    if state_obj is None:
        return None
    elif state_obj.state in {STATE_UNAVAILABLE, STATE_UNKNOWN}:
        return state_obj.state

    try:
        value = float(state_obj.state)
    except ValueError:
        return state_obj.state

    if normalize:
        unit = state_obj.attributes.get("unit_of_measurement")
        if len(unit) > 2:
            if unit[0] == "k":
                return value * 10**3
            elif unit[0] == "M":
                return value * 10**6

    return value
