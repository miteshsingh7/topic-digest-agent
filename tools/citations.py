from smolagents import tool

@tool
def generate_citations(sources: str) -> str:
    """Formats collected sources into a clean numbered references block.
    Takes a pipe-separated list of sources where each source is formatted as 'title|url'.
    
    Args:
        sources: A pipe-separated list of sources. Each source should be on a new line formatted as 'title|url'. Example: 'Article Title|https://example.com'
    """
    try:
        lines = [l.strip() for l in sources.strip().split("\n") if l.strip()]
        citations = []
        for i, line in enumerate(lines, 1):
            parts = line.split("|")
            if len(parts) >= 2:
                title = parts[0].strip()
                url = parts[1].strip()
                citations.append(f"[{i}] {title}\n    URL: {url}")
            else:
                citations.append(f"[{i}] {line}")
        
        if not citations:
            return "No valid sources provided for citation generation."
        
        header = "\n" + "=" * 50 + "\n📚 REFERENCES\n" + "=" * 50 + "\n\n"
        return header + "\n\n".join(citations)
    except Exception as e:
        return f"Error generating citations: {str(e)}"
