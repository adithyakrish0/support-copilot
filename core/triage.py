"""Triage engine: classify tickets and draft replies.

This module contains the logic to:
1. Classify a ticket by category and priority.
2. Decide if a ticket needs human escalation.
3. Draft an empathetic response grounded in the knowledge base.
"""

from __future__ import annotations

from core import kb, llm

SYSTEM_PROMPT = f"""You are an elite Support Operations Assistant for Northwind Cloud.
Your goal is to triage incoming tickets with high precision and empathy.

KNOWLEDGE BASE:
{kb.as_prompt_block()}

INSTRUCTIONS:
1. CATEGORIZE: Assign one category (Billing, Technical, Account, Onboarding).
2. PRIORITIZE: Assign priority (P0: Critical/Outage, P1: Urgent, P2: General).
3. ESCALATE: Set "escalate": true if:
   - The user is angry or threatening to cancel.
   - It is a security/2FA issue that only an owner can fix.
   - The request falls outside the Knowledge Base facts.
4. DRAFT: Write a short, empathetic reply grounded ONLY in the KB above.
   - If you don't know the answer from the KB, set "escalate": true and say you are handing it to a specialist.
   - DO NOT make up policies or features.

OUTPUT FORMAT:
Return ONLY a JSON object:
{{
  "category": "...",
  "priority": "...",
  "escalate": bool,
  "reason": "short explanation of priority/escalation",
  "draft": "your response to the customer"
}}
"""


def triage(ticket_text: str) -> dict:
    """Analyze a ticket and return the triage JSON.

    If no LLM key is set, falls back to mock rule-based logic.
    """
    cfg = llm.config()

    if not cfg["live"]:
        return _mock_triage(ticket_text)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"TICKET TEXT:\n{ticket_text}"},
    ]

    try:
        raw_response = llm.chat(messages)
        return llm.parse_json(raw_response)
    except Exception as e:
        return {{
            "category": "Unknown",
            "priority": "P2",
            "escalate": True,
            "reason": f"System error: {str(e)}",
            "draft": "I'm sorry, I'm having trouble processing your request right now. I've escalated this to a human agent who will get back to you shortly."
        }}


def _mock_triage(text: str) -> dict:
    """Fallback logic for when no LLM key is provided."""
    text_lower = text.lower()

    category = "General"
    priority = "P2"
    escalate = False
    reason = "Automated triage (Mock Mode)"

    if "bill" in text_lower or "refund" in text_lower:
        category = "Billing"
    elif "login" in text_lower or "password" in text_lower:
        category = "Account"
    elif "bug" in text_lower or "error" in text_lower:
        category = "Technical"

    if "cancel" in text_lower or "urgent" in text_lower or "presentation" in text_lower:
        priority = "P1"
        escalate = True
        reason = "High urgency or churn risk detected (Mock Mode)"

    return {
        "category": category,
        "priority": priority,
        "escalate": escalate,
        "reason": reason,
        "draft": "[MOCK REPLY] Thank you for your message. We are looking into your request regarding "
        + category
        + ". A specialist will follow up if needed.",
    }
