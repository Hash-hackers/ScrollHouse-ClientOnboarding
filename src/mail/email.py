import smtplib
from email.mime.text import MIMEText


def send_scrollhouse_welcome_email(
    generate_text,        # <- your Gemini text function
    smtp_email,
    smtp_password,
    client_name,
    brand_name,
    client_email,
    account_manager,
    kickoff_calendar_link,
):
    """
    Generates and sends Scrollhouse welcome email using any LLM.
    """

    # 1️⃣ Prompt for LLM
    prompt = f"""
Write a warm, professional welcome email.

Client name: {client_name}
Brand name: {brand_name}
Account manager: {account_manager}
Kickoff link: {kickoff_calendar_link}

Include:
• Welcome message
• Brief Scrollhouse process
• What happens in first 2 weeks
• Ask them to book kickoff call
• Friendly but professional tone
• 120–160 words
"""

    # 2️⃣ Generate email using Gemini/OpenAI/etc
    email_body = generate_text(prompt)
    subject = f"Welcome to Scrollhouse, {brand_name}! 🚀"

    # 3️⃣ Send email
    msg = MIMEText(email_body)
    msg["Subject"] = subject
    msg["From"] = smtp_email
    msg["To"] = client_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(smtp_email, smtp_password)
        server.send_message(msg)

    return {
        "status": "sent",
        "recipient": client_email,
        "subject": subject
    }
