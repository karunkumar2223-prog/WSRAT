from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """
    Validate whether the supplied URL contains
    a valid scheme and hostname.
    """
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)