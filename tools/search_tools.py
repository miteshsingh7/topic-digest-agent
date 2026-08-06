from smolagents import tool
from ddgs import DDGS
import requests
from markdownify import markdownify

@tool
def web_search(query: str) -> str:
    """Performs a web search for a given query and returns top search result titles, URLs, and snippets.
    
    Args:
        query: The search query to look up on the web.
    """
    try:
        with DDGS(timeout=5) as ddgs:
            results = list(ddgs.text(query, max_results=3))
        
        if not results:
            return f"No search results found for: {query}"
        
        formatted = []
        for r in results:
            title = r.get("title", "No Title")
            href = r.get("href", "")
            snippet = r.get("body", "")
            formatted.append(f"Title: {title}\nURL: {href}\nSnippet: {snippet}\n")
        
        return "\n---\n".join(formatted)
    except Exception as e:
        return f"Error performing web search for {query}: {str(e)}"

search_tool = web_search

@tool
def visit_webpage(url: str) -> str:
    """Fetches text content from a web URL including Wikipedia using custom browser headers.
    Returns clean text truncated to 1000 characters for fast token-efficient processing.
    
    Args:
        url: The full webpage URL to visit and read.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        text = markdownify(response.text)
        
        lines = [line.strip() for line in text.splitlines() if line.strip() and not line.startswith('*') and not line.startswith('[')]
        clean_text = " ".join(lines)
        
        max_chars = 1000
        if len(clean_text) > max_chars:
            clean_text = clean_text[:max_chars] + "\n... [content truncated]"
            
        return clean_text if clean_text else "Webpage loaded but contained no readable text."
    except Exception as e:
        return f"Error visiting webpage {url}: {str(e)}"

webpage_tool = visit_webpage
