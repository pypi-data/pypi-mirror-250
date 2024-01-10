"""
URL utilities
"""
import re
from typing import List, Optional
from urllib.parse import urlparse, ParseResult


def extract_urls(
    text: str, url_schemes: Optional[List[str]] = None
) -> List[ParseResult]:
    """
    Extract URLs from a string.
    """

    # URL schemes to match
    if url_schemes is None:
        url_schemes = [
            "http",
            "https",
            "ftp",
            "ftps",
            "sftp",
            "scp",
            "git",
            "ssh",
            "rsync",
        ]
    url_schemas_pattern = r"(?:" + ("|".join(url_schemes)) + r")"
    # Regular expression to match URLs
    url_pattern = re.compile(
        url_schemas_pattern
        + r":\/\/[-a-z0-9@:%._\+~#=]{1,256}\.[a-z]{1,6}\b[-a-z0-9()!@:%_\+.~#?&\/\/=]*",
        re.IGNORECASE,
    )

    # Find all matches in the text
    urls: List[str] = re.findall(url_pattern, text)

    # Parse the URLs using urlparse to get cleaner results
    parsed_urls: List[ParseResult] = []
    for url in urls:
        try:
            parsed_urls.append(urlparse(url))
        except ValueError:
            pass

    return parsed_urls
