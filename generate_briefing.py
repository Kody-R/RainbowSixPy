import ollama

def generate_mission_briefing(location,operation,objective,enemy):
    prompt = f"""
You are a tactical mission planner. Write a detailed and realistic Rainbow Six mission briefing in the style of Tom Clancy novels. Include:

- Operation name : {operation}
- Location : {location}
- Objective : {objective}
- Known threats : {enemy}
- Special considerations



Mission Briefing:
"""

    response = ollama.chat(
        model='mistral',
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']

# Example
briefing = generate_mission_briefing("Kingston,Jamaica", "Operation Lightning Bolt","Hostage rescue in a fortified embassy", "Jamaican Cartel")
print(briefing)
