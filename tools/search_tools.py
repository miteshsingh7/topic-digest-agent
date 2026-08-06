from smolagents import tool, DuckDuckGoSearchTool
import requests
from markdownify import markdownify

search_tool = DuckDuckGoSearchTool(max_results=5)

@tool
def visit_webpage(url: str) -> str:
    """Fetches full page text content from a given web URL, including Wikipedia.
    Converts HTML to clean text and returns up to 6000 characters for detailed analysis.
    
    Args:
        url: The full webpage URL to visit and read.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        text = markdownify(response.text)
        
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = "\n".join(lines)
        
        max_chars = 6000
        if len(clean_text) > max_chars:
            clean_text = clean_text[:max_chars] + "\n... [content truncated for detail]"
            
        return clean_text if clean_text else "Webpage loaded but contained no readable text."
    except Exception as e:
        return f"Error visiting webpage {url}: {str(e)}"

webpage_tool = visit_webpage
