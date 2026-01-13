def collect_user_profile():
    print("\nAnswer a few questions to personalize recommendations.\n")

    profile = {}
    profile["age"] = int(input("Age: "))
    profile["height_cm"] = int(input("Height (cm): "))
    profile["weight_kg"] = int(input("Weight (kg): "))
    profile["experience"] = input("Experience (beginner / intermediate / expert): ")
    profile["use_case"] = input("Main use (city / off-road / touring / work): ")
    profile["budget"] = int(input("Budget (USD): "))
    profile["country"] = input("Country: ")
    profile["preference"] = input("Style preference (sport / comfort / utility): ")

    return profile
