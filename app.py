import streamlit as st
import os
from dotenv import load_dotenv
from agent import create_agent
from tools.notes import get_research_log, clear_research_log
from smolagents import ActionStep

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

if "research_complete" not in st.session_state:
    st.session_state.research_complete = False
if "final_digest" not in st.session_state:
    st.session_state.final_digest = ""
if "steps_log" not in st.session_state:
    st.session_state.steps_log = []

col_topic, col_model = st.columns([3, 1])
with col_topic:
    topic = st.text_input("Enter Research Topic", placeholder="e.g. Applications of Quantum Computing in Drug Discovery")
with col_model:
    model_choice = st.selectbox(
        "Model",
        ["llama-3.3-70b", "mixtral-8x7b"],
        index=0
    )

selected_model = "groq/llama-3.3-70b-versatile" if model_choice == "llama-3.3-70b" else "groq/mixtral-8x7b-32768"

col1, col2 = st.columns([1, 4])
with col1:
    start_btn = st.button("🚀 Start Research", type="primary")
with col2:
    if st.button("🗑️ Clear Log"):
        clear_research_log()
        st.session_state.research_complete = False
        st.session_state.final_digest = ""
        st.session_state.steps_log = []
        st.rerun()

if start_btn and topic:
    clear_research_log()
    st.session_state.research_complete = False
    st.session_state.final_digest = ""
    st.session_state.steps_log = []
    
    status_box = st.status("🔬 Agent is conducting research...", expanded=True)
    
    with status_box:
        st.write("Initializing smolagents CodeAgent with Groq LLM...")
        agent = create_agent(api_key=api_key, model_id=selected_model)
        
        st.write("Executing ReAct research loop (Search → Visit → Extract → Verify → Synthesize)...")
        try:
            result = agent.run(topic)
            st.session_state.final_digest = str(result)
            
            steps = []
            for step in agent.memory.steps:
                if isinstance(step, ActionStep):
                    steps.append({
                        "number": getattr(step, 'step_number', len(steps) + 1),
                        "thought": getattr(step, 'model_output', None) or "(No reasoning)",
                        "tool_calls": str(getattr(step, 'tool_calls', None)) if getattr(step, 'tool_calls', None) else None,
                        "observation": str(getattr(step, 'observations', None)) if getattr(step, 'observations', None) else None
                    })
            
            st.session_state.steps_log = steps
            st.session_state.research_complete = True
            status_box.update(label="Research Complete! ✅", state="complete", expanded=False)
        except Exception as e:
            st.error(f"Error during agent execution: {str(e)}")
            status_box.update(label="Research Failed ❌", state="error", expanded=True)

if st.session_state.research_complete:
    st.markdown("---")
    st.subheader("📋 Research Digest")
    st.markdown(st.session_state.final_digest)
    
    st.download_button(
        "📥 Download Digest",
        data=st.session_state.final_digest,
        file_name=f"digest_{topic.replace(' ', '_')[:30]}.md",
        mime="text/markdown"
    )
    
    if st.session_state.steps_log:
        st.markdown("---")
        st.subheader("🧠 ReAct Reasoning Trace")
        for step in st.session_state.steps_log:
            with st.expander(f"Step {step['number']} Details", expanded=False):
                st.markdown(f"**Thought:** {step['thought']}")
                if step['tool_calls']:
                    st.markdown("**Tool Calls:**")
                    st.code(step['tool_calls'], language="python")
                if step['observation']:
                    st.markdown("**Observation:**")
                    obs_text = step['observation']
                    if len(obs_text) > 800:
                        obs_text = obs_text[:800] + "\n... [truncated]"
                    st.text(obs_text)

    logs = get_research_log()
    if logs:
        st.markdown("---")
        st.subheader("📝 Research Log")
        for item in logs:
            st.markdown(f"- **[{item['timestamp']}]** [{item['source']}]({item['source']}): {item['note']}")
