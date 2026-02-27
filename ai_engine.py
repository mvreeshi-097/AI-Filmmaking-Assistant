import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro")

def generate_film_package(idea):

    master_prompt = f"""
You are a professional Hollywood-level AI Film Production Assistant.

Based on this idea:
"{idea}"

Generate:

1. Full Scene-wise Screenplay
2. Character Bible (detailed psychological profiles)
3. Shot Breakdown (camera angles, lighting, mood)
4. Budget Estimate (low-mid budget realistic)
5. Production Schedule (day-wise)
6. Moodboard Visual Prompts (for AI image generation)
7. Casting Suggestions (Indian & International options)
8. Dialogue Style Guide (tone consistency rules)

Make everything structured with headings.
Be professional and cinematic.
"""

    response = model.generate_content(master_prompt)
    return response.text