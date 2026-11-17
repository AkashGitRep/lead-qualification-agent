import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()
MODEL = "claude-haiku-4-5"

SYSTEM_PROMPT = """You are a booking assistant for a turnkey interior design studio in Bengaluru, India.
Ask ONE question at a time, in this order: property type, scope, budget, start timeline, area in Bengaluru.
Plain text only. No markdown, no bold, no bullet lists. Keep each message to two sentences.
Budget options: under 10 lakh, 10 to 20 lakh, 20 to 40 lakh, above 40 lakh.
Start options: within 1 month, 1 to 6 months, later.
Area: any Bengaluru locality, for example Whitefield or Koramangala.
When all five answers are collected, reply with exactly: DONE"""

SAVE_LEAD_TOOL = {
    "name": "save_lead",
    "description": "Save the qualification answers for a finished lead.",
    "input_schema": {
        "type": "object",
        "properties": {
            "property": {"type": "string", "enum": ["apartment", "villa", "independent house"]},
            "scope": {"type": "string", "enum": ["full", "partial"]},
            "budget": {"type": "string", "enum": ["under 10 lakh", "10 to 20 lakh", "20 to 40 lakh", "above 40 lakh"]},
            "start": {"type": "string", "enum": ["within 1 month", "1 to 6 months", "later"]},
            "area": {"type": "string", "description": "The Bengaluru locality the user named"},
        },
        "required": ["property", "scope", "budget", "start", "area"],
    },
}

BENGALURU_AREAS = {
    "whitefield", "koramangala", "indiranagar", "hebbal", "jayanagar",
    "electronic city", "marathahalli", "hsr layout", "bellandur", "sarjapur",
    "yelahanka", "jp nagar", "bannerghatta", "rajajinagar", "malleshwaram", "btm layout",
}

def qualify(lead: dict) -> tuple[bool, str]:
    if lead["budget"] == "under 10 lakh":
        return False, "budget below minimum"
    if lead["start"] == "later":
        return False, "start too far out"
    area = lead["area"].lower()
    if not any(a in area for a in BENGALURU_AREAS):
        return False, "area not in service list"
    return True, "qualified"

def extract_lead(messages) -> dict:
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system="Read the conversation and call save_lead with the user's answers. Map budget and start to the closest allowed option.",
        tools=[SAVE_LEAD_TOOL],
        tool_choice={"type": "tool", "name": "save_lead"},
        messages=[{"role": "user", "content": json.dumps(messages)}],
    )
    for block in response.content:
        if block.type == "tool_use":
            return block.input
    raise RuntimeError("model did not call save_lead")

QUESTIONS = [
    ("property", "What type of property is it? (apartment, villa, independent house)"),
    ("scope", "Is this a full home fit-out or only some rooms? (full, partial)"),
    ("budget", "What is your budget? (under 10 lakh, 10 to 20 lakh, 20 to 40 lakh, above 40 lakh)"),
    ("start", "When do you want to start? (within 1 month, 1 to 6 months, later)"),
    ("area", "Which area of Bengaluru is the property in? (for example Whitefield or Koramangala)"),
]

FIXED_CHOICES = {
    "budget": ["under 10 lakh", "10 to 20 lakh", "20 to 40 lakh", "above 40 lakh"],
    "start": ["within 1 month", "1 to 6 months", "later"],
}

def ask(field: str, question: str) -> str:
    while True:
        answer = input(f"\nBot: {question}\nYou: ").strip().lower()
        if field not in FIXED_CHOICES:
            if answer:
                return answer
            print("Please type an answer.")
            continue
        # Accept a choice if the answer contains it, or matches its first word
        for choice in FIXED_CHOICES[field]:
            if answer == choice or answer.replace(" lakhs", " lakh") == choice:
                return choice
        print(f"Please pick one of: {', '.join(FIXED_CHOICES[field])}")

def run_conversation():
    lead = {}
    print("Hi! I can help you get a quote for your home interior.")
    for field, question in QUESTIONS:
        lead[field] = ask(field, question)
    print("\nLead:", lead)
    ok, reason = qualify(lead)
    print("Qualified:", ok, "-", reason)

if __name__ == "__main__":
    run_conversation()