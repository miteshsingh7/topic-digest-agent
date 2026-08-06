import streamlit as st
import os
from dotenv import load_dotenv
from agent import create_agent
from tools.notes import get_research_log, clear_research_log
from smolagents import ActionStep, FinalAnswerStep

load_dotenv()

st.set_page_config(
    page_title="Topic Digest Agent",
    page_icon="🔬",
    layout="centered"
)

st.title("🔬 Topic Digest Agent")
st.caption("AI-Powered Research Assistant (ReAct Framework)")

api_key = os.getenv("GROQ_API_KEY", "")
if not api_key:
    st.error("GROQ_API_KEY not found in .env file. Please add it to .env")
    st.stop()

topic = st.text_input("Enter Research Topic", placeholder="e.g. Applications of Quantum Computing in Drug Discovery")

col1, col2 = st.columns([1, 4])
with col1:
    start_btn = st.button("🚀 Start Research", type="primary")
with col2:
    if st.button("🗑️ Clear Log"):
        clear_research_log()
        st.rerun()

if start_btn and topic:
    clear_research_log()
    st.subheader(f"Researching: {topic}")
    
    agent = create_agent(api_key=api_key)
    steps_data = []
    final_answer = None
    
    status_container = st.status("Agent is working through ReAct loop...", expanded=True)
    
    with status_container:
        for step in agent.run(topic, stream=True):
            if isinstance(step, ActionStep):
                step_num = getattr(step, 'step_number', len(steps_data) + 1)
                thought = getattr(step, 'model_output', None) or "(No reasoning)"
                tool_calls = getattr(step, 'tool_calls', None)
                obs = getattr(step, 'observations', None)
                
                st.write(f"**Step {step_num}:** {thought}")
                if tool_calls:
                    st.code(str(tool_calls), language="python")
                if obs:
                    with st.expander(f"Observation (Step {step_num})", expanded=False):
                        st.write(obs)
                
                steps_data.append(step)
            elif isinstance(step, FinalAnswerStep):
                final_answer = step.output
                
        status_container.update(label="Research Complete! ✅", state="complete", expanded=False)

    if final_answer:
        st.markdown("---")
        st.subheader("📋 Research Digest")
        st.markdown(final_answer)
        
        st.download_button(
            "📥 Download Digest",
            data=str(final_answer),
            file_name=f"digest_{topic.replace(' ', '_')[:30]}.md",
            mime="text/markdown"
        )
    
    logs = get_research_log()
    if logs:
        st.markdown("---")
        st.subheader("📝 Research Log")
        for item in logs:
            st.markdown(f"- **[{item['timestamp']}]** [{item['source']}]({item['source']}): {item['note']}")
