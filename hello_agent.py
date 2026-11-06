from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  # reads ANTHROPIC_API_KEY from .env

client = Anthropic()

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=300,
    system="You are a friendly assistant for a dental clinic. Ask one question at a time to understand what the patient needs.",
    messages=[
        {"role": "user", "content": "Hi, I'm interested in veneers."}
    ],
)

print(response.content[0].text)