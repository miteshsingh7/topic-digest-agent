from smolagents import tool
import litellm
import os

@tool
def extract_key_facts(text: str, topic: str) -> str:
    """Extracts detailed, comprehensive facts from raw webpage text into structured bullet points.
    Uses an LLM to intelligently parse, analyze, and organize detailed information.
    
    Args:
        text: The raw text content from a webpage to extract facts from.
        topic: The research topic to focus the extraction on.
    """
    max_chars = 6000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n... [truncated]"
    
    prompt = f"""Extract detailed, comprehensive key facts from the text below regarding the topic: "{topic}"

Instructions:
- Provide 8 to 12 detailed, informative bullet points
- Include specific data, dates, technical details, statistics, and concepts where present
- Explain the background and context for each point
- Organize by key themes if appropriate

Text:
{text}

Detailed Key Facts:"""
    
    try:
        api_key = os.getenv("GROQ_API_KEY", "")
        response = litellm.completion(
            model="groq/llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            api_key=api_key,
            temperature=0.2,
            max_tokens=1200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error extracting facts: {str(e)}"
