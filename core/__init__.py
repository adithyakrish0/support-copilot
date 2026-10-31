"""Core logic for Support Copilot, kept separate from the Streamlit UI.

Modules:
    kb        - the mock knowledge base replies must be grounded in
    llm       - provider-agnostic (OpenAI-compatible) chat client
    triage    - classify a ticket and draft a reply
    evaluate  - score the assistant against a labelled test set
"""
