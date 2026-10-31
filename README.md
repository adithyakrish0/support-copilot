# Support Copilot + QA Scorecard 🤖📊

**A production-grade AI-Ops portfolio project demonstrating automated support triage and LLM evaluation.**

Live Demo: [Your Streamlit Cloud Link Here]
GitHub: [https://github.com/adithyakrish0/support-copilot](https://github.com/adithyakrish0/support-copilot)

---

## 🚀 The Problem
Customer support teams are flooded with tickets. Generic AI bots often "hallucinate" (make up facts) or fail to escalate urgent issues, leading to customer frustration and churn.

## 🛠️ The Solution
This project is a **Support Triage Engine** with a built-in **QA Scorecard**. It doesn't just answer tickets; it audits its own performance against a strict Knowledge Base (KB) and business rubric.

### Key Features:
1. **Intelligent Triage:** Auto-classifies tickets by Category (Billing, Technical, etc.) and Priority (P0-P2).
2. **Escalation Logic:** Detects angry users, churn threats, and security edge cases that require a human.
3. **QA Scorecard (LLM-as-a-Judge):** A secondary auditor model grades the triage output on:
   - **Grounding:** Did the bot stick to the facts in the KB?
   - **Escalation Accuracy:** Did it hand off the right tickets?
   - **Empathy & Goal Completion:** Is the response helpful and professional?
4. **Performance Dashboard:** Visualizes system-wide accuracy across a 15+ scenario test suite.

---

## 🏗️ Architecture & Stack
- **Frontend:** Streamlit (Python-based dashboard)
- **AI Models:** Groq (Llama 3.3 70B) for speed / OpenRouter for fallback.
- **Evaluation:** Custom "LLM-as-a-Judge" scoring engine.
- **Data:** CSV-based test suite with labeled ground truths.

---

## 🚦 Getting Started

### 1. Clone & Install
```bash
git clone https://github.com/adithyakrish0/support-copilot.git
cd support-copilot
pip install -r requirements.txt
```

### 2. Environment Setup
Copy `.env.example` to `.env` and add your **Groq API Key**.
*Note: If no key is provided, the app runs in **Mock Mode** for demonstration purposes.*

### 3. Run the App
```bash
streamlit run app.py
```

---

## 📈 Evaluation Results
The system is tested against a variety of messy, real-world scenarios:
- **P0 Outages:** Correctly identified and escalated.
- **Angry Users:** Detected sentiment and prioritized P1.
- **Hallucination Check:** Successfully flags responses that quote non-existent refund windows.

---

## 🧑‍💻 Author
**Adithyakrishnan P N**  
AI Operations & Customer Support Specialist  
[LinkedIn](https://www.linkedin.com/in/adithyakrishnanpn) | [Portfolio](https://github.com/adithyakrish0)
