import os
import time

from google import genai
from google.genai import errors


class AIServiceUnavailable(Exception):
    """Raised when the external AI provider cannot respond."""
    pass


def get_client():
    return genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )


def generate_text(prompt):
    client = get_client()

    primary_model = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash",
    )

    fallback_model = os.getenv(
        "GEMINI_FALLBACK_MODEL",
    )

    models = [primary_model]

    if fallback_model and fallback_model != primary_model:
        models.append(fallback_model)

    for model in models:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )

                if response.text:
                    return response.text.strip()

                raise AIServiceUnavailable(
                    "Gemini returned an empty response."
                )

            except errors.ServerError:
                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue

                break

            except errors.APIError as exc:
                raise AIServiceUnavailable(
                    "The AI service is currently unavailable."
                ) from exc

            except AIServiceUnavailable:
                raise

            except Exception as exc:
                raise AIServiceUnavailable(
                    "The AI service is currently unavailable."
                ) from exc

    raise AIServiceUnavailable(
        "The AI service is temporarily unavailable. "
        "Please try again shortly."
    )

def generate_lead_summary(lead):
    notes = lead.notes.all().order_by(
        "created_at"
    )

    note_text = "\n".join(
        f"- {note.content}"
        for note in notes
    )

    if not note_text:
        note_text = "No notes available."

    prompt = f"""
You are an assistant for a real-estate CRM.

Summarize this lead in 2-4 concise sentences.

Focus on:
- buyer intent
- property interest
- budget
- current pipeline status
- most important next action

Do not invent information.

Lead information:
Name: {lead.first_name} {lead.last_name}
Status: {lead.get_status_display()}
Source: {lead.get_source_display()}
Property interest: {lead.property_interest}
Budget: {lead.budget}
Follow-up date: {lead.follow_up_date}

Notes:
{note_text}
"""

    return generate_text(prompt)


def generate_follow_up(lead):
    notes = lead.notes.all().order_by(
        "-created_at"
    )[:5]

    note_text = "\n".join(
        f"- {note.content}"
        for note in notes
    )

    if not note_text:
        note_text = "No recent notes available."

    prompt = f"""
You are assisting a professional real-estate agent.

Write a short follow-up message for this lead.

Requirements:
- professional but natural
- concise
- suitable for WhatsApp or email
- do not invent property availability
- do not invent prices
- do not invent appointments
- do not invent facts not provided
- return only the message

Lead information:
Name: {lead.first_name} {lead.last_name}
Status: {lead.get_status_display()}
Property interest: {lead.property_interest}
Budget: {lead.budget}

Recent notes:
{note_text}
"""

    return generate_text(prompt)