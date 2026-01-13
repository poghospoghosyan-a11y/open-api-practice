def apply_rules(profile):
    warnings = []

    if profile["experience"] == "beginner" and profile["budget"] > 10000:
        warnings.append(
            "User is a beginner — recommend low to mid engine capacity vehicles."
        )

    if profile["age"] < 18:
        warnings.append(
            "User may be under legal riding age. Emphasize legal restrictions."
        )

    if profile["use_case"] == "off-road":
        warnings.append(
            "Focus on quads and dual-sport motorcycles."
        )

    return warnings
