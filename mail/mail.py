import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

load_dotenv()

def send_scrollhouse_welcome_email(
    client_name: str,
    brand_name: str,
    client_email: str,
    account_manager: str,
    kickoff_calendar_link: str,
):
    """
    Generates and sends Scrollhouse welcome email.
    """

    # 1️⃣ Generate email using LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)

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

    # 2️⃣ Send email via Gmail SMTP
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEText(email_body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = client_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

    return {
        "status": "success",
        "sent_to": client_email,
        "subject": subject
    }
