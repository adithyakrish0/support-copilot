"""Mock knowledge base for the fictional SaaS product "Northwind Cloud".

Every reply the assistant drafts is supposed to be grounded in these facts.
`core.evaluate` uses this text to detect unsupported claims (e.g. quoting a
refund window that does not exist anywhere in the policy).
"""

KB = {
    "refund_policy": (
        "Full refunds are available within 30 days of purchase. After 30 days we can "
        "only issue a prorated account credit, never a refund. Annual Enterprise "
        "contracts are non-refundable except as stated in the MSA."
    ),
    "password_reset": (
        "Users can reset their own password from the login screen via 'Forgot password'. "
        "The reset link expires after 15 minutes. Support agents never ask a customer "
        "for their password or a 2FA code."
    ),
    "plan_limits": "Starter includes 5 seats. Growth includes 25 seats. Enterprise includes unlimited seats.",
    "sla": (
        "Growth and Enterprise plans get P0: 1 hour, P1: 4 hours, P2: 1 business day. "
        "Starter plans are best-effort and carry no SLA guarantee."
    ),
    "data_export": "CSV and JSON exports are available under Settings > Data > Export.",
    "billing_portal": "Payment methods are updated under Settings > Billing > Payment Methods.",
    "security": (
        "Only the account owner can enable or change two-factor authentication. "
        "We never ask customers to share passwords or 2FA codes."
    ),
    "cancellation": (
        "Customers can cancel any time under Settings > Billing. Access continues until "
        "the end of the current billing period."
    ),
}


def as_prompt_block() -> str:
    """Render the KB as a numbered block for the LLM system prompt."""
    return "\n".join(f"- {key}: {value}" for key, value in KB.items())


def as_text() -> str:
    """Full KB as one string, used by the grounding check."""
    return " ".join(KB.values())
