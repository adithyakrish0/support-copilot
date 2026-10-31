import streamlit as st
import pandas as pd
import os
from core import triage, evaluate, llm

st.set_page_config(
    page_title="Support Copilot | QA Scorecard",
    page_icon="🤖",
    layout="wide"
)

# --- Sidebar ---
st.sidebar.title("Support Copilot")
st.sidebar.markdown("---")

cfg = llm.config()
if cfg["live"]:
    st.sidebar.success(f"Live Mode: {cfg['model']}")
else:
    st.sidebar.warning("Mock Mode (No API Key)")
    st.sidebar.info("Paste your key in .env to enable AI triage.")

st.sidebar.markdown("---")
st.sidebar.caption("v1.0.0 | AI Ops Portfolio")

# --- Main UI ---
st.title("🤖 Support Copilot + QA Scorecard")
st.markdown("""
This tool helps support teams triage tickets faster while maintaining a strict 
**QA Scorecard** to monitor AI performance.
""")

tab1, tab2 = st.tabs(["🚀 Live Triage", "📊 QA Scorecard"])

with tab1:
    st.header("Live Triage Assistant")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        ticket_input = st.text_area(
            "Paste Customer Ticket:",
            placeholder="e.g. I need a refund for my last invoice...",
            height=200
        )
        
        if st.button("Triage Ticket", type="primary"):
            if ticket_input:
                with st.spinner("AI is triaging..."):
                    result = triage.triage(ticket_input)
                    st.session_state['last_result'] = result
                    st.session_state['last_ticket'] = ticket_input
            else:
                st.error("Please enter a ticket first.")

    with col2:
        if 'last_result' in st.session_state:
            res = st.session_state['last_result']
            
            # Status Badges
            c1, c2, c3 = st.columns(3)
            c1.metric("Category", res.get("category", "Unknown"))
            c2.metric("Priority", res.get("priority", "P2"))
            
            if res.get("escalate"):
                c3.error("⚠️ Escalated")
            else:
                c3.success("✅ Auto-Resolved")
            
            st.markdown(f"**Reasoning:** {res.get('reason', 'N/A')}")
            
            st.markdown("---")
            st.subheader("Drafted Response:")
            st.info(res.get("draft", "No draft generated."))
            
            if st.button("Run Instant QA Check"):
                with st.spinner("Auditing draft..."):
                    qa = evaluate.evaluate_response(st.session_state['last_ticket'], res)
                    st.json(qa)

with tab2:
    st.header("System QA Performance Dashboard")
    st.markdown("Running the evaluation suite against the standard test set.")

    if st.button("Run Full QA Audit Suite"):
        test_file = "data/test_tickets.csv"
        if os.path.exists(test_file):
            df_test = pd.read_csv(test_file)
            
            with st.spinner(f"Auditing {len(df_test)} tickets..."):
                results_df = evaluate.run_full_suite(df_test)
                
                # --- Metrics ---
                m1, m2, m3, m4 = st.columns(4)
                
                avg_grounding = results_df["grounding_score"].mean()
                avg_escalation = results_df["escalation_score"].mean()
                avg_empathy = results_df["empathy_score"].mean()
                avg_goal = results_df["goal_met_score"].mean()
                
                m1.metric("Grounding (Accuracy)", f"{avg_grounding:.1%}")
                m2.metric("Escalation Accuracy", f"{avg_escalation:.1%}")
                m3.metric("Empathy Score", f"{avg_empathy:.1%}")
                m4.metric("Goal Completion", f"{avg_goal:.1%}")
                
                # --- Charts ---
                st.markdown("---")
                st.subheader("Score Breakdown")
                
                # Reshape for bar chart
                chart_data = pd.DataFrame({
                    "Metric": ["Grounding", "Escalation", "Empathy", "Goal Met"],
                    "Score": [avg_grounding, avg_escalation, avg_empathy, avg_goal]
                })
                st.bar_chart(chart_data.set_index("Metric"))
                
                # --- Detail Table ---
                st.markdown("---")
                st.subheader("Detailed Audit Log")
                st.dataframe(results_df, use_container_width=True)
                
                st.download_button(
                    label="Download Audit Report (CSV)",
                    data=results_df.to_csv(index=False),
                    file_name="qa_audit_report.csv",
                    mime="text/csv"
                )
        else:
            st.error("Test data file not found. Please ensure data/test_tickets.csv exists.")
