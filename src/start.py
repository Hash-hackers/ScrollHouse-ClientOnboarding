from google import genai

# Create Gemini client
client = genai.Client(api_key="AIzaSyBldSLbjEWtEhLLIvPon0GV-FyW5A1n4Ow")

def generate_text(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text
