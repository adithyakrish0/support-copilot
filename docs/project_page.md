# Project Showcase: Support Copilot + QA Scorecard

## Overview
As AI becomes central to customer support, the biggest risk is **reliability**. This project demonstrates how to build a support assistant that is "self-aware"—meaning it includes an automated quality assurance layer to ensure every response is grounded in truth and escalated when necessary.

## Why this matters for AI Ops
In an AI Operations role, my job is not just to "use AI," but to **ensure it works safely and accurately**. This project showcases:
- **Prompt Engineering:** Designing system instructions that enforce strict grounding.
- **Evaluation (LLM-as-a-Judge):** Building an automated auditor to replace manual ticket reviews.
- **Operations Thinking:** Mapping out escalation trees for P0 outages and security risks.

## The Triage Logic
The engine analyzes incoming text for three main vectors:
1. **Intent:** What does the user want? (Billing, Technical, etc.)
2. **Urgency:** How fast do they need it? (P0, P1, P2)
3. **Escalation:** Is this safe for a bot to handle, or does it need a human?

## The QA Scorecard
The "Scorecard" tab runs the engine against a labeled dataset of 15 messy tickets. It measures:
- **Grounding Accuracy:** 1.0 means 0% hallucinations.
- **Escalation Precision:** Did we miss any angry users?
- **Goal Completion:** Did the user actually get what they needed?

## Key Learnings
- **Negative Constraints are Critical:** Telling a bot "what NOT to do" is as important as telling it what to do.
- **Evaluation is a Feedback Loop:** The Scorecard helps identify which parts of the Knowledge Base are weak or confusing for the model.

---

*This project was built as part of my professional portfolio to demonstrate expertise in AI implementation, technical support, and data-driven operations.*
