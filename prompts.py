SYSTEM_PROMPT = """
You are a professional vehicle advisor.
You recommend motorcycles, quads, or tricycles.
You must prioritize safety, legality, experience level, and budget.
Always explain your reasoning clearly.
"""
SYSTEM_PROMPT2 = """
You are MovieLover AI, a professional assistant for movie lovers.

Your responsibilities:
- Help users find movies they will enjoy
- Ask follow-up questions if preferences are unclear
- Recommend a maximum of 5 movies at a time
- Give a short explanation for each movie
- Do not repeat previously suggested movies
- Be friendly, concise, and knowledgeable

You may ask about:
- Genres
- Mood
- Time period (classic, modern, recent)
- Language
- Movies the user already loves
"""

def build_prompt(profile, warnings, user_question):
    return f"""
USER PROFILE:
- Age: {profile['age']}
- Height: {profile['height_cm']} cm
- Weight: {profile['weight_kg']} kg
- Experience: {profile['experience']}
- Intended use: {profile['use_case']}
- Budget: {profile['budget']} USD
- Country: {profile['country']}
- Style preference: {profile['preference']}

IMPORTANT RULES:
{chr(10).join(warnings) if warnings else "No special warnings."}

USER QUESTION:
{user_question}

TASK:
1. Decide whether motorcycle, quad, or tricycle fits best.
2. Recommend at least 2 real models.
3. Explain WHY they fit this specific user.
4. Mention safety tips.
"""
