from smolagents import tool
from datetime import datetime

_research_log = []

@tool
def save_note(note: str, source_url: str) -> str:
    """Saves a research finding to the running research log.
    Each note is timestamped and linked to its source URL.
    
    Args:
        note: The research finding or observation to save.
        source_url: The URL where this finding came from.
    """
    entry = {
        "note": note,
        "source": source_url,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    _research_log.append(entry)
    return f"✅ Note saved ({len(_research_log)} total notes in research log)"

def get_research_log():
    return _research_log.copy()

def clear_research_log():
    _research_log.clear()
