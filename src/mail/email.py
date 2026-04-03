import smtplib
from email.mime.text import MIMEText


def send_scrollhouse_welcome_email(
    generate_text,        # function that calls Gemini
    smtp_email,           # your gmail
    smtp_password,        # gmail app password
    client_name,
    brand_name,
    client_email,
    account_manager,
    kickoff_calendar_link,
):
    """
    Generate and send Scrollhouse welcome email.
    """

    # 🧠 Prompt for Gemini
    prompt = f"""
Write a warm, professional welcome email.

Client name: {client_name}
Brand name: {brand_name}
Account manager: {account_manager}
Kickoff link: {kickoff_calendar_link}

The email must include:
• Welcome message
• Brief explanation of Scrollhouse process
• What happens in first 2 weeks
• Ask them to book kickoff call
• Friendly but professional tone
• 120–150 words
"""

    # ✍️ Generate email text using Gemini
    email_body = generate_text(prompt)

    # 📌 Email subject
    subject = f"Welcome to Scrollhouse, {brand_name}! 🚀"

    # 📤 Create email message
    msg = MIMEText(email_body)
    msg["Subject"] = subject
    msg["From"] = smtp_email
    msg["To"] = client_email

    # 📬 Send email using Gmail SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(smtp_email, smtp_password)
        server.send_message(msg)

    print(f"✅ Welcome email sent to {client_email}")
