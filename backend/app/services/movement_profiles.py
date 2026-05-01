"""
Movement Profile Registry

Maps vehicle types and explicit user selections to OSRM routing profiles.
This is the single source of truth for profile resolution — it ensures the
routing engine, ETA calculations, and API responses all use the same profile.

OSRM Profiles supported by a standard OSRM instance:
  - driving  (car / motor vehicles)
  - cycling  (bicycle)
  - walking  (foot)

Extending: Add new vehicle_type → profile mappings below to support trucks,
motorcycles, or custom profiles without changing any other service code.
"""

from typing import Literal

# Valid OSRM profiles for this system
VALID_PROFILES = {"driving", "cycling", "walking"}

# Map from vehicle_type (DB enum) to OSRM profile
VEHICLE_TYPE_TO_PROFILE: dict[str, str] = {
    "car":        "driving",
    "van":        "driving",
    "truck":      "driving",
    "motorcycle": "driving",
    "bicycle":    "cycling",
    # Future extensions:
    # "cargo_bike": "cycling",
    # "pedestrian_courier": "walking",
}

# Human-readable labels for the frontend
PROFILE_LABELS: dict[str, dict] = {
    "driving": {
        "label": "Driving",
        "icon":  "🚗",
        "description": "Optimized for motor vehicles using road network",
    },
    "cycling": {
        "label": "Cycling",
        "icon":  "🚴",
        "description": "Optimized for bicycles using bike-friendly paths",
    },
    "walking": {
        "label": "Walking",
        "icon":  "🚶",
        "description": "Optimized for pedestrians including shortcuts",
    },
}


def resolve_profile(
    explicit_profile: str | None,
    vehicle_type: str | None,
) -> str:
    """
    Resolve the OSRM routing profile from:
      1. An explicit user selection (highest priority)
      2. The vehicle type assigned to the route
      3. Default to 'driving'

    Args:
        explicit_profile: Profile explicitly requested in the API payload.
        vehicle_type:     Vehicle type string from the Vehicle model.

    Returns:
        A validated OSRM profile string: 'driving' | 'cycling' | 'walking'
    """
    # 1. Explicit selection from user / API request
    if explicit_profile and explicit_profile in VALID_PROFILES:
        return explicit_profile

    # 2. Derive from vehicle type
    if vehicle_type and vehicle_type in VEHICLE_TYPE_TO_PROFILE:
        return VEHICLE_TYPE_TO_PROFILE[vehicle_type]

    # 3. Safe default
    return "driving"


def get_profile_metadata(profile: str) -> dict:
    """Return human-readable metadata for a given profile."""
    return PROFILE_LABELS.get(profile, PROFILE_LABELS["driving"])
