from anthropic import Anthropic
from dotenv import load_dotenv
import json

load_dotenv()
client = Anthropic()

SYSTEM_PROMPT = """You are a booking assistant for a turnkey interior design studio in Bengaluru, India.
Ask ONE question at a time, in this order: property type, scope, budget, start timeline, area in Bengaluru (for example Whitefield or Koramangala).
Plain text only. No markdown, no bold, no bullet lists. Keep each message to two sentences.
Budget options: under 10 lakh, 10 to 20 lakh, 20 to 40 lakh, above 40 lakh.
Start options: within 1 month, 1 to 6 months, later.
After the user answers the area question, reply with exactly: DONE"""

def run_conversation():
    messages = [{"role": "user", "content": "Hi, I want a quote for my home interior."}]
    while True:
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=200,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        reply = response.content[0].text.strip()
        if "DONE" in reply:
            break
        print(f"\nBot: {reply}")
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": input("You: ").strip()})

    
    extract = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        system="Extract the lead's answers. Reply with raw JSON only, no code fences, keys: property, scope, budget, start, area. Use the user's words.",
        messages=[{"role": "user", "content": str(messages)}],
    )
    raw = extract.content[0].text.strip().strip("`")
    if raw.startswith("json"):
        raw = raw[4:]
    print("Raw extraction:", raw)
    try:
        answers = json.loads(raw)
    except json.JSONDecodeError:
        print("Could not parse answers. Check the raw output above.")
        return
    print("Qualified:", qualify(answers))

MIN_BUDGET_LAKH = 10
SERVICE_AREA = "bengaluru"

def qualify(answers: dict) -> bool:
    budget_ok = "under 10" not in answers.get("budget", "").lower()
    timeline_ok = "later" not in answers.get("start", "").lower()
    area_ok = SERVICE_AREA in answers.get("area", "").lower()
    return budget_ok and timeline_ok and area_ok

if __name__ == "__main__":
    run_conversation()