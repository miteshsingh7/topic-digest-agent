from smolagents import tool
from urllib.parse import urlparse

HIGH_CREDIBILITY = {
    ".gov", ".gov.uk", ".gov.au", ".gov.in", ".gov.ca",
    ".edu", ".ac.uk", ".ac.in", ".edu.au",
    "who.int", "cdc.gov", "nih.gov", "nasa.gov", "nsf.gov",
    "nature.com", "science.org", "sciencedirect.com",
    "pubmed.ncbi.nlm.nih.gov", "scholar.google.com",
    "ieee.org", "acm.org", "arxiv.org", "springer.com",
    "thelancet.com", "bmj.com", "nejm.org",
    "reuters.com", "apnews.com", "bbc.com", "bbc.co.uk",
    "britannica.com", "nationalgeographic.com",
    "un.org", "worldbank.org", "imf.org",
}

MEDIUM_CREDIBILITY = {
    "ibm.com", "microsoft.com", "google.com", "apple.com",
    "nytimes.com", "theguardian.com", "washingtonpost.com",
    "wsj.com", "economist.com", "forbes.com", "bloomberg.com",
    "cnn.com", "cnbc.com", "aljazeera.com", "dw.com",
    "ft.com", "time.com", "newsweek.com", "usatoday.com",
    "theatlantic.com", "newyorker.com", "npr.org", "pbs.org",
    "arstechnica.com", "wired.com", "techcrunch.com",
    "theverge.com", "zdnet.com", "cnet.com", "engadget.com",
    "thenextweb.com", "venturebeat.com", "hbr.org",
    "wikipedia.org", "stackoverflow.com", "stackexchange.com",
    "developer.mozilla.org", "docs.python.org",
    "github.com", "medium.com",
}

LOW_CREDIBILITY = {
    "reddit.com", "twitter.com", "x.com", "facebook.com",
    "instagram.com", "tiktok.com", "pinterest.com",
    "quora.com", "yahoo.com/answers",
    "buzzfeed.com", "dailymail.co.uk",
    "bit.ly", "tinyurl.com", "t.co", "goo.gl",
}

@tool
def check_source_credibility(url: str) -> str:
    """Evaluates the credibility of a source URL based on domain reputation.
    Returns a credibility rating (High/Medium/Low) with reasoning.
    
    Args:
        url: The full URL of the source to evaluate.
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower().replace("www.", "")
        
        for tld in [".gov", ".edu", ".ac.uk", ".ac.in"]:
            if domain.endswith(tld):
                return f"⭐⭐⭐ HIGH CREDIBILITY\nSource: {domain}\nReason: Official {tld} domain — government or academic institution. Generally highly trustworthy."
        
        for known in HIGH_CREDIBILITY:
            if known in domain:
                return f"⭐⭐⭐ HIGH CREDIBILITY\nSource: {domain}\nReason: Recognized authoritative source — established institution, peer-reviewed publication, or major wire service."
        
        for known in MEDIUM_CREDIBILITY:
            if known in domain:
                return f"⭐⭐ MEDIUM CREDIBILITY\nSource: {domain}\nReason: Established publication or well-known platform. Generally reliable but may have editorial bias. Cross-reference important claims."
        
        for known in LOW_CREDIBILITY:
            if known in domain:
                return f"⭐ LOW CREDIBILITY\nSource: {domain}\nReason: Social media, user-generated content, or unverified source. Information should be independently verified."
        
        if domain.endswith(".org"):
            return f"⭐⭐ MEDIUM CREDIBILITY\nSource: {domain}\nReason: .org domain — could be a reputable organization but .org is open to anyone. Verify the organization's reputation."
        
        return f"⭐ LOW CREDIBILITY\nSource: {domain}\nReason: Unknown or unrecognized domain. Could not verify source reputation. Treat information with caution and cross-reference."
        
    except Exception as e:
        return f"⚠️ UNABLE TO ASSESS\nError parsing URL: {str(e)}"
