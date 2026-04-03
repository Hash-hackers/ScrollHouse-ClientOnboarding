import smtplib
from email.mime.text import MIMEText
from langchain.schema import HumanMessage


def send_scrollhouse_welcome_email(
    llm,                       # pass ChatOpenAI() from main app
    smtp_email,                # sender email
    smtp_password,             # app password
    client_name,
    brand_name,
    client_email,
    account_manager,
    kickoff_calendar_link,
):
    """
    Generates and sends the Scrollhouse welcome email.
    Returns dict with send status.
    """

    # 1️⃣ Generate email using LLM
    prompt = f"""
Write a warm, professional welcome email.

Client name: {client_name}
Brand name: {brand_name}
Account manager: {account_manager}
Kickoff link: {kickoff_calendar_link}

The email must include:
• Welcome message
• Brief Scrollhouse process
• What happens in first 2 weeks
• Ask them to book kickoff call
"""

    email_body = llm.invoke([HumanMessage(content=prompt)]).content
    subject = f"Welcome to Scrollhouse, {brand_name}! 🚀"

    # 2️⃣ Send email
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
