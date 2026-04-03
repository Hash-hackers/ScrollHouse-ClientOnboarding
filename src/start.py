from google import genai
from mail.email import send_scrollhouse_welcome_email

# Gemini setup
client = genai.Client(api_key="AIzaSyBldSLbjEWtEhLLIvPon0GV-FyW5A1n4Ow")

def generate_text(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text


# Call the email sender
send_scrollhouse_welcome_email(
    generate_text=generate_text,
    smtp_email="markus39107.com",
    smtp_password="kkpx iadl iktk qbti",
    client_name="Aisha",
    brand_name="GlowLab",
    client_email="aisha@glowlab.com",
    account_manager="Rohan",
    kickoff_calendar_link="https://calendly.com/kickoff"
)
