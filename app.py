import streamlit as st
import json
import os
from dotenv import load_dotenv

from agent_quant import run_quant_agent
from agent_risk import run_risk_agent
from agent_pm import run_portfolio_manager

# Page Configuration
st.set_page_config(
    page_title="AI Investment Committee",
    page_icon="📈",
    layout="wide"
)

st.title("🤖 Multi-Agent AI Investment Committee")
st.caption("Institutional Equity Analysis Engine powered by Gemini 2.5 & Live Market Grounding")

# Sidebar Configuration
st.sidebar.header("Committee Settings")
ticker_input = st.sidebar.text_input("US Equity Ticker", value="PLTR").upper()
run_button = st.sidebar.button("Run Committee Review", type="primary")

st.sidebar.markdown("---")
st.sidebar.markdown("### Agent Architecture")
st.sidebar.markdown("**Agent A:** Quant Fundamental Analyst")
st.sidebar.markdown("**Agent B:** Sovereign Macro & News Auditor")
st.sidebar.markdown("**Agent C:** CIO & Portfolio Manager")

if run_button and ticker_input:
    st.markdown(f"## Executive Review: **${ticker_input}**")
    
    # Live Status Console (Shows real-time agent progression)
    with st.status("Executing Multi-Agent Workflow...", expanded=True) as status:
        
        # Step 1: Agent A
        st.write("📊 **Agent A (Quant Analyst)** evaluating financial statements & Rule of 40...")
        try:
            quant_report = run_quant_agent(ticker_input)
            st.success("Agent A Evaluation Complete!")
        except Exception as e:
            st.error(f"Agent A Failed: {e}")
            st.stop()
            
        # Step 2: Agent B
        st.write("🌍 **Agent B (Macro Risk Officer)** scanning breaking RSS news & risk vectors...")
        try:
            risk_report = run_risk_agent(ticker_input, quant_report)
            st.success("Agent B Audit Complete!")
        except Exception as e:
            st.error(f"Agent B Failed: {e}")
            st.stop()
            
        # Step 3: Agent C
        st.write("👨‍💼 **Agent C (Portfolio Manager)** adjudicating debate & rendering verdict...")
        try:
            memo = run_portfolio_manager(ticker_input, quant_report, risk_report)
            st.success("Committee Review Finalized!")
            status.update(label="Committee Review Complete!", state="complete", expanded=False)
        except Exception as e:
            st.error(f"Agent C Failed: {e}")
            st.stop()

    # --- TOP CALLOUT METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Final Decision", memo.final_decision)
    with col2:
        st.metric("Conviction Score", f"{memo.conviction_score}/100")
    with col3:
        st.metric("Recommended Allocation", f"{memo.recommended_allocation_pct}%")
    with col4:
        st.metric("Human Override Required?", "YES ⚠️" if memo.human_in_the_loop_flag else "NO ✅")

    st.markdown("---")

    # --- DETAILED AGENT TABS ---
    tab1, col_sep, tab2, col_sep2, tab3 = st.tabs(["👨‍💼 Investment Memo (Agent C)", " ", "📊 Fundamental Math (Agent A)", " ", "🛡️ Risk & Headlines (Agent B)"])

    with tab1:
        st.subheader("Synthesis & Final Decision Rationale")
        st.info(memo.quant_vs_risk_synthesis)
        
        if memo.human_in_the_loop_flag:
            st.warning("⚠️ **Governance Flag:** Extreme multiples or high macro risk detected. Human-in-the-loop signoff mandatory before order execution.")

    with tab2:
        st.subheader("Quantitative Scorecard")
        st.write(f"**Fundamental Score:** {quant_report.fundamental_score}/100")
        st.write(f"**Rule of 40 Score:** {quant_report.rule_of_40_score}%")
        st.write(f"**Free Cash Flow Yield:** {quant_report.fcf_yield_pct}%")
        st.write(f"**Trailing P/E:** {quant_report.pe_ratio}")
        st.write(f"**Trailing P/S:** {quant_report.ps_ratio}")
        st.markdown("**Quant Summary:**")
        st.write(quant_report.quant_summary)

    with tab3:
        st.subheader("Macro & News Audit")
        st.write(f"**Macro Headwind Score:** {risk_report.macro_headwind_score}/100")
        
        st.markdown("**Identified Risk Vectors:**")
        for r in risk_report.identified_risks:
            st.markdown(f"- **[{r.severity}] {r.category}:** {r.description}")
            
        st.markdown("**Bear Case Thesis:**")
        st.error(risk_report.bear_case_thesis)

else:
    st.info("👈 Enter a ticker in the sidebar and click **Run Committee Review** to launch the agents.")