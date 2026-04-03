from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)

send_scrollhouse_welcome_email(
    llm=llm,
    smtp_email="yourgmail@gmail.com",
    smtp_password="app_password",
    client_name="Aisha",
    brand_name="GlowLab",
    client_email="aisha@glowlab.com",
    account_manager="Rohan",
    kickoff_calendar_link="https://calendly.com/kickoff"
)
