from smolagents import tool
from openai import OpenAI
import os

@tool
def extract_key_facts(text: str, topic: str) -> str:
    """Extracts concise key facts from raw webpage text into structured bullet points.
    Uses LLM to organize essential information efficiently.
    
    Args:
        text: The raw text content from a webpage to extract facts from.
        topic: The research topic to focus the extraction on.
    """
    max_chars = 1200
    if len(text) > max_chars:
        text = text[:max_chars] + "\n... [truncated]"
    
    prompt = f"""Extract key facts from the text below regarding: "{topic}"

Instructions:
- Provide 5 to 7 concise, informative bullet points
- Focus on facts, data, and key takeaways

Text:
{text}

Key Facts:"""
    
    try:
        api_key = os.getenv("GROQ_API_KEY", "")
        client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=350
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error extracting facts: {str(e)}"
