import os
import smtplib
from typing import TypedDict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI


# -----------------------------
# 1. LOAD SECRETS
# -----------------------------
load_dotenv("config/secrets.env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in config/secrets.env")

if not GMAIL_ADDRESS:
    raise ValueError("GMAIL_ADDRESS not found in config/secrets.env")

if not GMAIL_APP_PASSWORD:
    raise ValueError("GMAIL_APP_PASSWORD not found in config/secrets.env")


# -----------------------------
# 2. LLM SETUP
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY
)


# -----------------------------
# 3. STATE DEFINITION
# -----------------------------
class OnboardingState(TypedDict, total=False):
    brand_name: str
    manager_name: str
    client_email: str
    email_subject: str
    email_body: str
    send_status: str


# -----------------------------
# 4. NODE 1 - GENERATE EMAIL
# -----------------------------
def generate_welcome_email(state: OnboardingState) -> OnboardingState:
    brand_name = state["brand_name"]
    manager_name = state["manager_name"]

    prompt = f"""
Write a professional and friendly welcome email for a new client.

Details:
- Brand Name: {brand_name}
- Account Manager Name: {manager_name}

The email must include:
1. A warm welcome to the client
2. Mention that {manager_name} will be their account manager
3. A short explanation of the Scrollhouse onboarding process
4. What the client can expect in the first two weeks
5. A positive and professional closing

Do not include any calendar link.
Do not include placeholders.
Keep it concise, polished, and business-friendly.
"""

    response = llm.invoke(prompt)

    return {
        **state,
        "email_subject": f"Welcome to Scrollhouse, {brand_name}",
        "email_body": response.content
    }


# -----------------------------
# 5. NODE 2 - SEND EMAIL VIA GMAIL
# -----------------------------
def send_email_gmail(state: OnboardingState) -> OnboardingState:
    receiver_email = state["client_email"]
    subject = state["email_subject"]
    body = state["email_body"]

    msg = MIMEMultipart()
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, receiver_email, msg.as_string())

        return {
            **state,
            "send_status": f"Email sent successfully to {receiver_email}"
        }

    except Exception as e:
        return {
            **state,
            "send_status": f"Failed to send email: {str(e)}"
        }


# -----------------------------
# 6. BUILD LANGGRAPH
# -----------------------------
graph = StateGraph(OnboardingState)

graph.add_node("generate_email", generate_welcome_email)
graph.add_node("send_email", send_email_gmail)

graph.set_entry_point("generate_email")
graph.add_edge("generate_email", "send_email")
graph.add_edge("send_email", END)

app = graph.compile()



if __name__ == "__main__":
    initial_state = {
        "brand_name": "Nike",
        "manager_name": "John Doe",
        "client_email": "client@example.com"
    }

    result = app.invoke(initial_state)

    print("\n--- EMAIL SUBJECT ---")
    print(result["email_subject"])

    print("\n--- EMAIL BODY ---")
    print(result["email_body"])

    print("\n--- STATUS ---")
    print(result["send_status"])
