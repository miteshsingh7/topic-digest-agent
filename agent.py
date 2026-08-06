import os
from smolagents import CodeAgent, OpenAIServerModel
from tools import (
    search_tool, webpage_tool, 
    extract_key_facts, check_source_credibility,
    save_note, generate_citations
)

SYSTEM_PROMPT_ADDITION = """
You are a research agent. Given a research topic, produce a structured research digest.

Follow this research workflow:
1. SEARCH: Perform 1 web_search.
2. VISIT: Use visit_webpage on 1 URL.
3. EXTRACT: Use extract_key_facts to get bullet points.
4. VERIFY: Use check_source_credibility on the URL.
5. LOG: Use save_note to save findings.
6. CITE: Use generate_citations to list references.
7. SYNTHESIZE: Write a clean final research digest with Executive Summary, Key Findings, Credibility Notes, and References.

Keep reasoning concise and steps efficient.
"""

def create_agent(api_key: str = None, model_id: str = "llama-3.1-8b-instant"):
    key = api_key or os.getenv("GROQ_API_KEY", "")
    if key:
        os.environ["GROQ_API_KEY"] = key
    
    model = OpenAIServerModel(
        model_id=model_id,
        api_base="https://api.groq.com/openai/v1",
        api_key=key
    )
    
    tools = [
        search_tool,
        webpage_tool,
        extract_key_facts,
        check_source_credibility,
        save_note,
        generate_citations
    ]
    
    agent = CodeAgent(
        tools=tools,
        model=model,
        max_steps=3,
        additional_authorized_imports=["re", "json", "datetime", "urllib"],
        verbosity_level=1
    )
    
    agent.prompt_templates["system_prompt"] = (
        agent.prompt_templates["system_prompt"] + SYSTEM_PROMPT_ADDITION
    )
    
    return agent
