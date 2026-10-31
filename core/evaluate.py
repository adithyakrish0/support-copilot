"""QA Scorecard Evaluation Engine.

This module acts as the "LLM-as-a-Judge". It evaluates the output of the
triage engine against a strict rubric.

Rubrics:
1. Grounding: Does the reply contain facts NOT found in the KB?
2. Escalation Accuracy: Did it correctly escalate (or fail to escalate)?
3. Goal Completion: Did it actually address the user's core problem?
4. Tone & Empathy: Is the language professional yet empathetic?
"""

from __future__ import annotations

import pandas as pd
from core import kb, llm

EVAL_PROMPT = f"""You are a Senior Support Quality Auditor.
Your task is to evaluate a Support Assistant's triage and response.

KNOWLEDGE BASE (Ground Truth):
{kb.as_text()}

TICKET TO EVALUATE:
{{ticket_text}}

ASSISTANT'S OUTPUT:
{{triage_output}}

EVALUATION RUBRIC:
1. GROUNDING (0-1): 1 if every fact in the draft is supported by the KB. 0 if it makes up a policy or detail.
2. ESCALATION (0-1): 1 if the escalation choice was correct (e.g. escalated angry user, did NOT escalate basic FAQ).
3. EMPATHY (0-1): 1 if the tone is helpful and professional. 0 if robotic or dismissive.
4. GOAL_MET (0-1): 1 if the core user question was answered correctly.

OUTPUT FORMAT:
Return ONLY a JSON object:
{{
  "grounding_score": int,
  "escalation_score": int,
  "empathy_score": int,
  "goal_met_score": int,
  "feedback": "one sentence explanation of the scores"
}}
"""


def evaluate_response(ticket_text: str, triage_output: dict) -> dict:
    """Evaluate a single triage result using the Evaluator LLM."""
    cfg = llm.config()

    if not cfg["live"]:
        return {
            "grounding_score": 1,
            "escalation_score": 1,
            "empathy_score": 1,
            "goal_met_score": 1,
            "feedback": "Mock evaluation (Scorecard active).",
        }

    messages = [
        {
            "role": "system",
            "content": "You are a strict QA auditor for customer support AI.",
        },
        {
            "role": "user",
            "content": EVAL_PROMPT.format(
                ticket_text=ticket_text, triage_output=str(triage_output)
            ),
        },
    ]

    try:
        raw_response = llm.chat(messages, temperature=0.0)  # Use 0 temp for consistency
        return llm.parse_json(raw_response)
    except Exception as e:
        return {
            "grounding_score": 0,
            "escalation_score": 0,
            "empathy_score": 0,
            "goal_met_score": 0,
            "feedback": f"Evaluation error: {str(e)}",
        }


def run_full_suite(test_data: pd.DataFrame) -> pd.DataFrame:
    """Run the triage + evaluation for an entire dataset.

    Returns a DataFrame with results and scores.
    """
    from core.triage import triage

    results = []

    for _, row in test_data.iterrows():
        ticket_text = row["ticket_text"]
        triage_out = triage(ticket_text)
        scores = evaluate_response(ticket_text, triage_out)

        combined = {
            "ticket": ticket_text,
            "category": triage_out.get("category"),
            "priority": triage_out.get("priority"),
            "escalated": triage_out.get("escalate"),
            "draft": triage_out.get("draft"),
            **scores,
        }
        results.append(combined)

    return pd.DataFrame(results)
