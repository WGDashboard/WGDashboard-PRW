#!/bin/env python3

from typing import Any


LEGACY_CONFIG_KEYS: dict[tuple[str, str], str] = {
    ("server", "auth_req"): "authentication_required",
    ("server", "dashboard_api_key"): "wgdashboard_apikey",
    ("server", "app_ip"): "hostname",
    ("server", "app_port"): "port",
}


def normalize_config_keys(config_data: dict[str, Any]) -> dict[str, Any]:
    '''Return config data with legacy keys replaced by canonical keys.'''
    normalized = {
        str(section).lower(): dict(values)
        for section, values in config_data.items()
        if isinstance(values, dict)
    }

    for (section, legacy_key), canonical_key in LEGACY_CONFIG_KEYS.items():
        section_values = normalized.get(section)
        if section_values is None or legacy_key not in section_values:
            continue

        if canonical_key not in section_values:
            section_values[canonical_key] = section_values[legacy_key]

        del section_values[legacy_key]

    return normalized
