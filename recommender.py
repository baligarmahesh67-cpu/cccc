"""Input validation and transparent rule-based crop ranking."""
import math

from crop_data import CROP_PROFILES, SEASONS, SOIL_TYPES, WATER_LEVELS


class InputValidationError(ValueError):
    """Raised when submitted farm parameters are missing or invalid."""


def _normalise_choice(value, allowed, field_name):
    if not isinstance(value, str) or not value.strip():
        raise InputValidationError(f"Please select {field_name}.")
    lookup = {item.lower(): item for item in allowed}
    result = lookup.get(value.strip().lower())
    if result is None:
        options = ", ".join(allowed)
        raise InputValidationError(f"Invalid {field_name}. Choose one of: {options}.")
    return result


def _rainfall_score(rainfall, low, high):
    """Return 25 inside the configured band, tapering to zero outside it."""
    if low <= rainfall <= high:
        return 25
    distance = low - rainfall if rainfall < low else rainfall - high
    return max(0, round(25 - (distance / max(high - low, 1)) * 25))


def recommend_crops(data, limit=5):
    if not isinstance(data, dict):
        raise InputValidationError("Please submit valid form values.")

    soil = _normalise_choice(data.get("soil_type"), SOIL_TYPES, "soil type")
    season = _normalise_choice(data.get("season"), SEASONS, "season")
    water = _normalise_choice(data.get("water_availability"), WATER_LEVELS, "water availability")

    raw_rainfall = data.get("rainfall_mm")
    if isinstance(raw_rainfall, bool):
        raise InputValidationError("Rainfall must be a number between 0 and 5000 mm.")
    try:
        rainfall = float(raw_rainfall)
    except (TypeError, ValueError):
        raise InputValidationError("Enter expected seasonal rainfall in millimetres.")
    if not math.isfinite(rainfall) or not 0 <= rainfall <= 5000:
        raise InputValidationError("Rainfall must be a finite number between 0 and 5000 mm.")

    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 10:
        raise InputValidationError("Result limit must be a whole number between 1 and 10.")

    scored = []
    for crop in CROP_PROFILES:
        score = 0
        reasons = []

        if soil in crop["soil_types"]:
            score += 35
            reasons.append(f"Soil type ({soil}) is included in this crop's profile")

        if season in crop["seasons"]:
            score += 25
            reasons.append(f"Season ({season}) matches this crop's profile")

        rain_points = _rainfall_score(rainfall, *crop["rainfall_mm"])
        score += rain_points
        if rain_points == 25:
            reasons.append("Entered rainfall falls within the prototype screening band")
        elif rain_points > 0:
            reasons.append("Entered rainfall is near the prototype screening band")
        else:
            reasons.append("Entered rainfall is outside the prototype screening band")

        if water in crop["water"]:
            score += 15
            reasons.append(f"Water availability ({water}) matches this crop's profile")
        else:
            reasons.append(f"Water availability ({water}) is not the preferred level in this crop's profile")

        # A crop with neither matching soil nor season is not useful as a result.
        if soil not in crop["soil_types"] and season not in crop["seasons"]:
            continue

        scored.append({
            "name": crop["name"],
            "match_score": min(score, 100),
            "description": crop["description"],
            "reasons": reasons,
            "evidence": crop["evidence"],
            "source": crop["source"],
            "prototype_rainfall_band_mm": crop["rainfall_mm"],
        })

    scored.sort(key=lambda item: (-item["match_score"], item["name"]))
    return scored[:limit]
